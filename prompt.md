System Prompt: You are an network configuration operator. And you will find error(s) and guarantees the correctness of planned or current network configurations.
User Prompt: The network configuration is below:
----
{config}
----
Pls help me find the most possible error(s) in the configuration and help me correct it.
The answer format should be a json like below and pls only return json:
    {{
        Correctness: '' // Yes, if there is any error and No, if there is no error.
        RootCause: '' // The top five error(s) with their line number, content and explaination of the error(s). If there are less than five errors, don't need to list five ones and pls list as many as you have.
    }}
    e.g.
    {{
        Correctness: 'Yes' 
        RootCause: ["1. Line 53 with 'ip address 2.1.324.2 255.255.255.255' has an invalid IP address, the reason is that the third octet of the IP address is 324, which exceeds the maximum value of 255 for an octet."...]
    }}