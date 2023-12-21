You may encounter errors like invalid range for IP, invalid syntax, invalid character insertion, functional misconfig and so on.
For invalid character insertion, some characters like @, %, ^, &, (, ), / may be mistyped into the config.
e.g., "%" is mistyped into the config "%version 15.2"
"/" is mistyped into "ip prefix-list inbound_route_filter seq 5 deny 2.0.0.0/8 le 32