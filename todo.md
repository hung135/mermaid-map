```mermaid
graph TD
    subgraph dialetc
     kubn
     MSSQL
     STOREPROC
     Python
    end
     
json-->flow_chart.md
sql-->simple_ddl-parser-->json 
    json-->kubn-->flow_chart.md
    json-->MSSQL-->flow_chart.md
    json-->STOREPROC-->flow_chart.md
    json-->Python-->flow_chart.md
    pythonfile--->dict--->json
```