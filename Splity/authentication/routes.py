from authlib.integrations.flask_client import OAuth
from flask import Blueprint, render_template, flash, redirect, url_for, current_app, session
from flask_login import login_user, logout_user, current_user, login_required
from Splity.forms.forms import LoginForm, RegistrationForm, ProfileNameForm
from Splity.services import authentication_services
from Splity.adapters.repository import UserRepository

authentication_blueprint=Blueprint("authentication",__name__)
oauth=OAuth()
oauth.register(name="google",server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",client_kwargs={"scope":"openid email profile"})

def _google_ready():
    return bool(current_app.config.get("GOOGLE_CLIENT_ID") and current_app.config.get("GOOGLE_CLIENT_SECRET"))

@authentication_blueprint.route("/register",methods=["GET","POST"],strict_slashes=False)
def register():
    if current_user.is_authenticated: return redirect(url_for("home.home"))
    if _google_ready(): return redirect(url_for("authentication.login"))
    form=RegistrationForm()
    if form.validate_on_submit():
        try:
            authentication_services.add_user_service(form.name.data,form.username.data,form.email.data,form.password.data)
            flash("Account created. Please log in.","success"); return redirect(url_for("authentication.login"))
        except authentication_services.AuthenticationException as error: flash(str(error),"danger")
    return render_template("authentication/register.html",form=form)

@authentication_blueprint.route("/login",methods=["GET","POST"],strict_slashes=False)
def login():
    if current_user.is_authenticated: return redirect(url_for("home.home"))
    form=LoginForm()
    if not _google_ready() and form.validate_on_submit():
        try:
            login_user(authentication_services.authenticate_user_service(form.username.data,form.password.data))
            return redirect(url_for("home.home"))
        except authentication_services.AuthenticationException as error: flash(str(error),"danger")
    return render_template("authentication/authentication.html",form=form,google_ready=_google_ready())

@authentication_blueprint.get("/auth/google")
def google_login():
    if not _google_ready():
        flash("Google sign-in has not been configured yet.","danger"); return redirect(url_for("authentication.login"))
    return oauth.google.authorize_redirect(url_for("authentication.google_callback",_external=True))

@authentication_blueprint.get("/auth/google/callback")
def google_callback():
    try:
        token=oauth.google.authorize_access_token()
        profile=token.get("userinfo") or oauth.google.userinfo()
    except Exception:
        flash("Google sign-in could not be completed. Please try again.","danger")
        return redirect(url_for("authentication.login"))
    google_sub=profile.get("sub"); email=profile.get("email")
    if not google_sub or not email or not profile.get("email_verified",False):
        flash("A verified Google email is required.","danger"); return redirect(url_for("authentication.login"))
    user=UserRepository().get_by_google_sub(google_sub)
    if user:
        login_user(user); return redirect(url_for("home.home"))
    session["pending_google"]={"sub":google_sub,"email":email,"suggested_name":profile.get("name","")}
    return redirect(url_for("authentication.complete_profile"))

@authentication_blueprint.route("/complete-profile",methods=["GET","POST"])
def complete_profile():
    pending=session.get("pending_google")
    if not pending: return redirect(url_for("authentication.login"))
    form=ProfileNameForm()
    if not form.is_submitted(): form.name.data=pending.get("suggested_name","")
    if form.validate_on_submit():
        try:
            user=authentication_services.add_google_user_service(form.name.data,pending["email"],pending["sub"])
            session.pop("pending_google",None); login_user(user)
            return redirect(url_for("home.home"))
        except authentication_services.AuthenticationException as error: flash(str(error),"danger")
    return render_template("authentication/complete_profile.html",form=form,email=pending["email"])

@authentication_blueprint.post("/logout")
@login_required
def logout():
    logout_user(); return redirect(url_for("authentication.login"))
