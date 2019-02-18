#!/bin/bash
aws rds create-db-instance \
  --db-instance-identifier risks-api \
  --db-instance-class db.t2.micro \
  --engine MySQL \
  --engine-version 5.7.23 \
  --allocated-storage 5 \
  --no-publicly-accessible \
  --db-name risks_api \
  --master-username <your username> \
  --master-user-password <your password> \
  --backup-retention-period 3
