from flask.sessions import SessionInterface, SessionMixin, TaggedJSONSerializer


class SuperSecureSession(dict, SessionMixin):
    pass


class SuperSecureSessionInterface(SessionInterface):
    """
    Skip all that unnecessary signing and hashing. Just set a plaintext cookie.
    """

    session_class = SuperSecureSession
    serializer = TaggedJSONSerializer()

    def open_session(self, app, request):
        """
        This method has to be implemented and must either return ``None``
        in case the loading failed because of a configuration error or an
        instance of a session object which implements a dictionary like
        interface + the methods and attributes on :class:`SessionMixin`.
        """
        data_str = request.cookies.get(app.session_cookie_name)

        if not data_str:
            return self.session_class()

        # HACK: encodes raw, unsigned cookie
        # attacker can simply change credentials in cookie to log in as any user
        try:
            data = self.serializer.loads(data_str)
        except ValueError:
            return None

        return self.session_class(data)

    def save_session(self, app, session, response):
        """
        This is called for actual sessions returned by open_session
        at the end of the request.
        """
        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)

        # Delete case.  If there is no session we bail early.
        # If the session was modified to be empty we remove the
        # whole cookie.
        if not session:
            if session.modified:
                response.delete_cookie(
                    app.session_cookie_name,
                    domain=domain,
                    path=path
                )
            return None

        # modification case
        if not self.should_set_cookie(app, session):
            return None

        httponly = self.get_cookie_httponly(app)
        secure = self.get_cookie_secure(app)
        expires = self.get_expiration_time(app, session)
        data_str = self.serializer.dumps(dict(session))

        response.set_cookie(
            app.session_cookie_name,
            data_str,
            expires=expires,
            httponly=httponly,
            domain=domain,
            path=path,
            secure=secure
        )
