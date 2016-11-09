#!/usr/bin/env python
# -*- coding: utf-8 -*-
import boto3

ec2 = boto3.client('ec2')
max_snapshot_num=7

target_volume='vol-0b396e3818161be54'

snapshots = ec2.describe_snapshots(Filters=[{'Name':'volume-id','Values':['vol-0b396e3818161be54']}])

# sorted(snapshots['Snapshots'], key=lambda a: a['StartTime'])
def filter_delete_targets(snapshots, max_snapshot_num):
    if(max_snapshot_num >= len(snapshots)):
        return []

