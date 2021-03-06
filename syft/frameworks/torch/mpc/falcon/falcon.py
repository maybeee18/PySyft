import syft

from syft.frameworks.torch.mpc.falcon.falcon_helper import FalconHelper


def conv2d(filters: syft.ReplicatedSharingTensor, image, padding=0):
    is_wrapper = filters.is_wrapper or image.is_wrapper

    if filters.is_wrapper:
        filters = filters.child

    if image.is_wrapper:
        image = image.child

    image_batches, image_channels, image_width, image_height = image.shape
    channels_out, filter_channels, filter_width, filter_height = filters.shape
    image = FalconHelper.unfold(image, filter_height, padding)
    filters = filters.view(channels_out, -1)
    result = filters @ image
    output_size = (image_height - filter_height + 2 * padding) + 1
    result = result.view(-1, channels_out, output_size, output_size)

    if is_wrapper:
        result = result.wrap()
    return result
