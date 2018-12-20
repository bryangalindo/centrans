
!K::
Gui, New
Gui, Add, Text,, Agent
Gui, Add, DropDownList, vAgent, PDQD|PDTJ
Gui, Add, Button, Default gOK1, OK
Gui, Show
RETURN


OK1:
Gui, Submit, nohide
PDQDArray := {AGENTREF: "PDQDJM", AGENT: "PUDONG TRANS (QD)", LOADPORT: "57047", CARRIER: {"APL": {MBL: "APLU", AGENTREF: "PDQDJMQJ"}, "ONE": {MBL: "ONEYTA8PK0", AGENTREF: "PDQDJMON"}, "CMA": {MBL: "CMDUQDJY", AGENTREF: "PDQDJMCM"}, "MSC": {MBL: "MEDUQ", AGENTREF: "PDQDJMMS"}, "MAERSK": {MBL: "MAEU", AGENTREF: "PDQDJMMK"}, "COSCO": {MBL: "COSU619", AGENTREF: "PDQDJMCO"}, "HAPAG": { MBL: "HLCUTA" . MONTH . "8", AGENTREF: "PDQDJMQQ"}, "ZIM": {MBL: "ZIMUQIN", AGENTREF: "PDQDJMBS"}}}

Agents := {PDQD: PDQDArray}
UserSubmittedAgent = %Agent%
MsgBox, % Agents[UserSubmittedAgent].AGENTREF

RETURN