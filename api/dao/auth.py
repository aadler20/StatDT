import bcrypt
import jwt
from datetime import datetime

from flask import current_app

from api.exceptions.badrequest import BadRequestException
from api.exceptions.validation import ValidationException

from neo4j.exceptions import ConstraintError


class AuthDAO:
    """
    The constructor expects an instance of the Neo4j Driver, which will be
    used to interact with Neo4j.
    """

    def __init__(self, driver, jwt_secret):
        self.driver = driver
        self.jwt_secret = jwt_secret

    """
    This method should create a new User node in the database with the email and username
    provided, along with an encrypted version of the password and a `userId` property
    generated by the server.

    The properties also be used to generate a JWT `token` which should be included
    with the returned user.
    """

    # tag::register[]
    def register(self, email, plain_password):
        def get_user_for_registration(tx, email):
            result = tx.run("MATCH (u:User {email: $email}) RETURN u",
                            email=email).single()
            if result is None:
                return None

            user = result.get('u')
            return user

        with self.driver.session() as session:
            user = session.read_transaction(get_user_for_registration, email=email)

        print(user)
        # User already exists, return exception
        if user:
            return None

        encrypted = bcrypt.hashpw(plain_password.encode("utf8"), bcrypt.gensalt()).decode('utf8')

        print('encrypted = ', encrypted)

        def create_user(tx, email, encrypted, username):
            return tx.run(""" // (1)
                CREATE (u:User {
                    email: $email,
                    password: $encrypted,
                    username: $username
                })
                RETURN u
            """, email=email, encrypted=encrypted, username=username).single()

        try:
            with self.driver.session() as session:
                username = email
                index_at = email.find('@')
                if index_at != -1:
                    username = email[:index_at]

                result = session.write_transaction(create_user, email, encrypted, username)

                user = result['u']

                payload = {
                    "email": user["email"],
                    "username": user["username"],
                    "password": user["password"]

                }

                payload["token"] = self._generate_token(payload)

                return payload
        except ConstraintError as err:
            # Pass error details through to a ValidationException
            raise ValidationException(err.message, {
                "email": err.message
            })

    # end::register[]

    """
    This method should attempt to find a user by the email address provided
    and attempt to verify the password.

    If a user is not found or the passwords do not match, a `false` value should
    be returned.  Otherwise, the users properties should be returned along with
    an encoded JWT token with a set of 'claims'.

    {
      userId: 'some-random-uuid',
      email: 'graphacademy@neo4j.com',
      username: 'GraphAcademy User',
      token: '...'
    }
    """

    # tag::authenticate[]
    def authenticate(self, email, plain_password):
        def get_user_for_login(tx, email):
            result = tx.run("MATCH (u:User {email: $email}) RETURN u",
                            email=email).single()
            if result is None:
                return None

            # Get the `u` value returned by the Cypher query
            user = result.get("u")

            return user

        with self.driver.session() as session:
            user = session.read_transaction(get_user_for_login, email=email)

            # User not found, return False
            if user is None:
                return False

            # Passwords do not match, return false
            if bcrypt.checkpw(plain_password.encode('utf-8'), user["password"].encode('utf-8')) is False:
                return False

            # Generate JWT Token
            payload = {
                "email": user["email"],
                "username": user["username"]
            }

            payload["token"] = self._generate_token(payload)
            print('payload in login:')
            print(payload)
            return payload

    # end::authenticate[]

    """
    This method should take the claims encoded into a JWT token and return
    the information needed to authenticate this user against the database.
    """

    # tag::generate[]
    def _generate_token(self, payload):

        # iat = datetime.utcnow()
        # payload["sub"] = payload["userId"]
        # payload["iat"] = iat
        # payload["nbf"] = iat
        # payload["exp"] = iat + current_app.config.get('JWT_EXPIRATION_DELTA')

        return jwt.encode(
            payload,
            self.jwt_secret,
            algorithm='HS256'
        ).decode('ascii')

    # end::generate[]

    """
    This method will attemp to decode a JWT token
    """

    # tag::decode[]
    def decode_token(self, auth_token):
        jwt_secret = self.jwt_secret
        print('jwt_secret in decode_token: ' + jwt_secret)
        try:
            payload = jwt.decode(auth_token, jwt_secret)
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    # end::decode[]
