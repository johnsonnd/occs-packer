import boto3
import re
import argparse
from getpass import getpass


def snapshots_matching_description(ec2, owner, description_expr):
    snapshots = set()
    for snapshot in ec2.snapshots.filter(OwnerIds=[str(owner)]):
        if re.match(description_expr, snapshot.description):
            snapshots.add(snapshot.id)
    return snapshots


def snapshots_registered_to_an_image(ec2, owner):
    snapshots = set()
    for image in ec2.images.filter(Owners=[str(owner)]):
        for block_device in image.block_device_mappings:
            if 'Ebs' in block_device:
                snapshots.add(block_device['Ebs']['SnapshotId'])
    return snapshots


def remove_snapshots(ec2, snapshot_ids):
    for snapshot_id in snapshot_ids:
        snapshot = ec2.Snapshot(snapshot_id)
        # snapshot.load()
        snapshot.delete()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('operation', choices=('list', 'remove'))
    parser.add_argument('--owner', metavar='OWNER_ID', default=765460880451)
    parser.add_argument('--region', metavar='REGION_NAME', default='us-east-1')
    return parser.parse_args()


def main():

    opts = parse_args()
    owner = opts.owner
    region = opts.region
    ec2 = boto3.resource("ec2", region_name=region)

    registered_snapshot_ids = snapshots_registered_to_an_image(ec2, owner)
    aws_vmimport_snapshots = snapshots_matching_description(ec2, owner, 'Created by AWS-VMImport service')
    copied_for_ami_snapshots = snapshots_matching_description(ec2, owner, 'Copied for DestinationAmi')
    imported_snapshot_ids = aws_vmimport_snapshots.union(copied_for_ami_snapshots)
    unregistered_snapshot_ids = imported_snapshot_ids.difference(registered_snapshot_ids)

    if opts.operation == 'list':
        print("\nRegistered image snapshots:")
        for snapshot_id in registered_snapshot_ids:
            print("   %s" % snapshot_id)

        print("\nUnregistered image snapshots:")
        for snapshot_id in unregistered_snapshot_ids:
            print("   %s" % snapshot_id)

    elif opts.operation == 'remove':

        print("\nUnregistered image snapshots:")
        for snapshot_id in unregistered_snapshot_ids:
            print("   %s" % snapshot_id)
        remove = getpass("\nRemove snapshots above? [yN] ")
        if remove == 'y' or remove == 'Y':
            print("Removing snapshots...")
            remove_snapshots(ec2, unregistered_snapshot_ids)


if __name__ == '__main__':
    main()
