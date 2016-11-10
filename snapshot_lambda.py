import datetime

# This script deletes the snapshots 
# created before the time repesented by currenttime - the following timedelta
before = datetime.timedelta(days=7)
# Represents the id of a volume.
# this script creates a snapshot of it, and deletes those of it
target_volume='vol-03f231d63dbfd7a25'

import boto3
import dateutil

def find_ids_of_snapshots(snapshots, timedelta):
    boundary = datetime.datetime.now(dateutil.tz.tz.tzutc()) - timedelta
    deleted_snapshots = filter(lambda snapshot: snapshot['StartTime'] < boundary, snapshots)
    return map(lambda snapshot: snapshot['SnapshotId'], deleted_snapshots)

def create_snapshot(client, volume_id):
    created = client.create_snapshot(VolumeId = volume_id, 
            Description='a snapshot created by ' + __file__ +' at ' + str(datetime.datetime.utcnow()) + '(UTC)')

    print('created a snapshot[snapshot id:' + created['SnapshotId'] + ']')

def delete_snapshots(client, snapshot_ids):
    for snapshot_id in snapshot_ids:
        print('delete the snapshot[snapshot id:' + snapshot_id + ']')
        client.delete_snapshot(SnapshotId=snapshot_id)

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    create_snapshot(ec2, target_volume) 
    snapshots = ec2.describe_snapshots(Filters=[{'Name':'volume-id','Values':[target_volume]}])
    delete_ids = find_ids_of_snapshots(snapshots['Snapshots'], before)
    delete_snapshots(ec2, delete_ids)
