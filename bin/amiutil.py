import boto3
import argparse


def get_images(ec2, owner, builder=None, build=None, release=None):
    filters = list()
    if builder:
        filters.append({'Name': 'tag:builder', 'Values': [builder]})
    if build:
        filters.append({'Name': 'tag:build', 'Values': [build]})
    if release:
        filters.append({'Name': 'tag:release', 'Values': [release]})

    return ec2.images.filter(Owners=[str(owner)], Filters=filters)


def get_image_timestamp(image):
    for tag in image.tags:
        if tag['Key'] == 'timestamp':
            return int(tag['Value'])
    return None


def get_latest_image(image_iter):
    latest_timestamp = None
    latest_image = None

    for image in image_iter:
        timestamp = get_image_timestamp(image)
        if timestamp is not None:
            if latest_timestamp is None:
                latest_timestamp = timestamp
                latest_image = image
            elif timestamp > latest_timestamp:
                latest_timestamp = timestamp
                latest_image = image
    return latest_image


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('operation', choices=('list', 'latest', 'taglatest'))
    parser.add_argument('--owner', metavar='OWNER_ID', default=765460880451)
    parser.add_argument('--region', metavar='REGION_NAME', default='us-east-1')
    parser.add_argument('--builder', metavar='TAG_VALUE', default=None)
    parser.add_argument('--build', metavar='TAG_VALUE', default=None)
    parser.add_argument('--release', metavar='TAG_VALUE', default=None)
    parser.add_argument('--output', metavar='OUTPUT', choices=('id', 'brief'), default='brief')
    return parser.parse_args()


def print_image_id(image):
    print(image.id)


def print_image_briefly(image):
    print("\n%s  \"%s\"" % (image.id, image.name))
    for tag in image.tags:
        print("  %s: %s" % (tag['Key'], tag['Value']))


__print_func_map = {
    'id': print_image_id,
    'brief': print_image_briefly
}


def main():
    opts = parse_args()
    owner = opts.owner
    region = opts.region
    operation = opts.operation
    print_image = __print_func_map[opts.output]

    ec2 = boto3.resource("ec2", region_name=region)
    image_iter = get_images(ec2, owner=owner, builder=opts.builder, build=opts.build, release=opts.release)

    if operation == 'list':
        for image in image_iter:
            print_image(image)
    elif operation == 'latest':
        image = get_latest_image(image_iter)
        if image is not None:
            print_image(image)
    elif operation == 'taglatest':
        print('Not yet implemented')

if __name__ == '__main__':
    main()
