# sql-to-csv-converter
## Purpose
This script serves to convert a SQL dump created by [HeidiSQL](https://www.heidisql.com/) and consisting of (many) `INSERT` statements into CSV to allow for easier import in other tools. I had a very large dataset (~10 GB, >100 million lines) to export and convert so for performance reasons neither a direct CSV export from a regular HeidiSQL query nor a table export from PhpMyAdmin was an option.

## Usage

````
python sql_to_csv.py -s source.sql -t output.csv
````

The script will find the first `INSERT` statement in `source.sql` and derive the column names from it. All subsequent `...VALUES...` statements are converted into comma-separated lines which are stripped off remaining SQL syntax such as brackets. HeidiSQL portions the `INSERT`s in batches of 10,000 lines. Column names mentioned in any `INSERT` after the first are ignored to keep the CSV clean.

## Example
Sample input (from HeidiSQL > Tools > [Export Database as SQL](https://www.heidisql.com/screenshots.php?which=export_sql), see `sample.sql` for full example):
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
The output file is only touched every 10,000 lines yielding a significant performance increase versus saving every line individually. Converting 110,000,000 lines took 12 minutes, i.e. approx. 150,000 items per second.