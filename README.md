# sql-to-csv-converter
## Purpose
The tool serves to convert a SQL dump created by [HeidiSQL](https://www.heidisql.com/) into CSV to allow for easier import in other tools. I had a very large dataset (~10 GB, >100 million lines) to export and convert hence for performance reasons neither a direct CSV export from a regular HeidiSQL query nor a table export from PhpMyAdmin was an option.

## Usage

````
python sql_to_csv.py -s source.sql -t output.csv
````

## Example
Sample input (from HeidiSQL > Tools > Export Database as SQL, see `sample.sql` for full example):
```
INSERT INTO `table_name` (`statusID`, `status`, `equipment`, `timestamp`, `user`, `seconds_since_last`) VALUES
        (769506, 'ACTIVE', 10457770, '2018-01-02 16:50:42', '', 720706),
        (769514, 'ACTIVE', 10458220, '2018-01-02 16:50:47', '', 720705);

INSERT INTO `table_name` (`statusID`, `status`, `equipment`, `timestamp`, `user`, `seconds_since_last`) VALUES
        (769506, 'ACTIVE', 10457770, '2018-01-02 16:50:42', '', 720706),
        (769507, 'ACTIVE', 10457810, '2018-01-02 16:50:42', '', 720705);
```

Sample output (see `sample.csv` for full example):
```
statusID,status,equipment,timestamp,user,seconds_since_last
769506,'ACTIVE',10457770,'2018-01-02 16:50:42','',720706
769507,'ACTIVE',10457810,'2018-01-02 16:50:42','',720705
769506,'ACTIVE',10457770,'2018-01-02 16:50:42','',720706
769507,'ACTIVE',10457810,'2018-01-02 16:50:42','',720705
```

## Performance
The tool processes roughly 60,000 lines from the target per second. The output file is only touched every 10,000 lines yielding a significant performance increase versus saving every line individually.