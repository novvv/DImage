import image
import time


def initialize(context):

    """Initialize the DImage product.
    This makes the object apear in the product list"""
    
    context.registerClass(
        image.DImage,
        constructors = (
            image.manage_addImageForm,
            image.manage_addImageAction,
            ),
        icon='www/Image_icon.gif'
    )
