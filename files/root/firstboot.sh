#!/bin/bash

cat > /root/firstboot << FIRSTBOOT
#!/bin/bash

PATH=/sbin:/bin:/usr/sbin:/usr/bin
export PATH

agent_key=e309d850571ce5dc8af3fbad1eb47c0ddda02fedf46f815f0028f6d842a30f27
nessus_host=nlmnessusmgr10.nlm.nih.gov
nessus_group=AWS_OCCS

/opt/nessus_agent/sbin/nessuscli agent link --key=${agent_key} --host=${nessus_host} --port=443 --groups=${AWS_OCCS}

sleep 10

systemctl enable nessusagent
systemctl start nessusagent

systemctl disable firstboot

rm -f /etc/systemd/system/firstboot.service
rm -f /root/firstboot
FIRSTBOOT

chmod 700 /root/firstboot

cat > /etc/systemd/system/firstboot.service << SYSTEMDFIRSTBOOT
[Unit]
Description=Finish Boostrapping Nessus Agent
After=salt-master.service

[Service]
Type=oneshot
ExecStart=/root/firstboot

[Install]
WantedBy=multi-user.target
SYSTEMDFIRSTBOOT

systemctl enable firstboot
