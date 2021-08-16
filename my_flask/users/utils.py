import os
from PIL import Image
from flask import url_for
from flask_mail import Message
from my_flask import app, mail


def save_account_image(image_file):
    image_name = image_file.filename
    image_path = os.path.join(app.root_path, "static/profile_images", image_name)

    # resize profile image using pillow module
    output_size = (125, 125)
    i = Image.open(image_file)
    i.thumbnail(output_size)

    i.save(image_path)
    return image_name


def send_email(user):
    print(type(user))
    token = user.get_token()
    msg = Message(
        subject="Reset password",
        recipients=[user.email],
        sender="noreply@gmail.com",
        body=f""" To reser your password follow the link below

    .....

    {url_for('users.reset_token', token=token, _external=True)}

    If you didn't sent a password reset request please ignore this message

    
    
    
     """,
    )
    mail.send(msg)
