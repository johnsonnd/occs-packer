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


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('operation', choices=('list', 'latest', 'taglatest'))
    parser.add_argument('--owner', metavar='OWNER_ID', default=765460880451)
    parser.add_argument('--region', metavar='REGION_NAME', default='us-east-1')
    parser.add_argument('--builder', metavar='TAG_VALUE', default=None)
    parser.add_argument('--build', metavar='TAG_VALUE', default=None)
    parser.add_argument('--release', metavar='TAG_VALUE', default=None)
    parser.add_argument('--raw', action='store_true', default=False)
    return parser.parse_args()


def main():
    opts = parse_args()
    owner = opts.owner
    region = opts.region
    operation = opts.operation

    ec2 = boto3.resource("ec2", region_name=region)
    image_iter = get_images(ec2, owner=owner, builder=opts.builder, build=opts.build, release=opts.release)

    if operation == 'list':
        for image in image_iter:
            if opts.raw:
                print(image.id)
            else:
                print("\n%s  \"%s\"" % (image.id, image.name))
                for tag in image.tags:
                    print("  %s: %s" % (tag['Key'], tag['Value']))
    elif operation == 'latest':
        print('Not yet implemented')
    elif operation == 'taglatest':
        print('Not yet implemented')

if __name__ == '__main__':
    main()
