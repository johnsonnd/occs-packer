import boto3
import re


def snapshots_matching_description(ec2, owner, description_expr):
    for snapshot in ec2.snapshots.filter(OwnerIds=[str(owner)]):
        if re.match(description_expr, snapshot.description):
            yield snapshot


def snapshots_registered_to_an_image(ec2, owner):
    snapshots = set()
    for image in ec2.images.filter(Owners=[str(owner)]):
        for block_device in image.block_device_mappings:
            if 'Ebs' in block_device:
                snapshots.add(block_device['Ebs']['SnapshotId'])
    return snapshots


def main():

    owner = 765460880451
    region = "us-east-1"
    ec2 = boto3.resource("ec2", region_name=region)

    print("\nSnapshots currently registered to an image:")
    registered_snapshot_ids = snapshots_registered_to_an_image(ec2, owner)
    for snapshot_id in registered_snapshot_ids:
        print("   %s" % snapshot_id)
    imported_snapshot_ids = set()

    print("\nSnapshots created by AWS-VMImport:")
    aws_vmimport_snapshots = snapshots_matching_description(ec2, owner, 'Created by AWS-VMImport service')
    for snapshot in aws_vmimport_snapshots:
        imported_snapshot_ids.add(snapshot.id)
        print("   %s" % snapshot.id)

    print("\nSnapshots created by copying:")
    copied_for_ami_snapshots = snapshots_matching_description(ec2, owner, 'Copied for DestinationAmi')
    for snapshot in copied_for_ami_snapshots:
        imported_snapshot_ids.add(snapshot.id)
        print("   %s" % snapshot.id)

    print("\nSnapshots that probably can go:")
    for snapshot_id in imported_snapshot_ids.difference(registered_snapshot_ids):
        print("   %s" % snapshot_id)


if __name__ == '__main__':
    main()
