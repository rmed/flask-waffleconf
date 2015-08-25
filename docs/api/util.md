#### ***def json_iter(obj)***

Create an iterator for a JSON object that is compatible with both Python 2 and
Python 3.

##### Parameters

- `obj`: JSON object to iterate

##### Returns

Iterator

---

#### ***parse_type(ctype, value)***

Parse the configuration according to the type specified.

##### Parameters

- `ctype`: string identifying the data type of the variable. Available types:

    - Boolean   ~> bool
    - Float     ~> float
    - Integer   ~> int
    - JSON      ~> json
    - Strings   ~> str

- `value`: string representation of the value to parse.

##### Returns

Parsed result
