# ohsome API Reference Guide

**Complete Reference for OSM Data Analysis via ohsome API**

## Base URL
```
https://api.ohsome.org/v1/
```

## API Endpoint Structure Tree
```
https://api.ohsome.org
└── v1
    ├── elements
    │   ├── area, count, length, perimeter
    │   │   ├── density
    │   │   │   ├── groupBy/boundary
    │   │   │   │   └── groupBy/tag
    │   │   │   ├── groupBy/tag
    │   │   │   └── groupBy/type
    │   │   ├── groupBy/key
    │   │   ├── groupBy/boundary
    │   │   │   └── groupBy/tag
    │   │   ├── groupBy/tag
    │   │   ├── groupBy/type
    │   │   └── ratio
    │   │       └── groupBy/boundary
    │   ├── bbox
    │   ├── centroid
    │   └── geometry
    ├── users
    │   └── count
    │       ├── density
    │       │   ├── groupBy/boundary
    │       │   ├── groupBy/tag
    │       │   └── groupBy/type
    │       ├── groupBy/boundary
    │       ├── groupBy/key
    │       ├── groupBy/tag
    │       └── groupBy/type
    ├── contributions
    │   ├── count
    │   │   └── density
    │   ├── bbox
    │   ├── centroid
    │   ├── geometry       
    │   └── latest
    │       ├── bbox
    │       ├── centroid
    │       ├── geometry
    │       └── count
    │           └── density
    ├── elementsFullHistory
    │   ├── bbox
    │   ├── centroid
    │   └── geometry
    └── metadata
```

## Common Parameters

### Boundary Parameters (choose one)
⚠️ **Required**: One (and only one) boundary parameter must be specified. No default value.

**Coordinate System**: WGS 84 (lon, lat format)

#### bboxes
Bounding box(es) defined by bottom-left and top-right corners.

**Formats**:
1. Simple: `lon1,lat1,lon2,lat2|lon1,lat1,lon2,lat2|...`
   ```
   8.5992,49.3567,8.7499,49.4371|9.1638,49.113,9.2672,49.1766
   ```

2. Named: `id1:lon1,lat1,lon2,lat2|id2:lon1,lat1,lon2,lat2|...`
   ```
   Heidelberg:8.5992,49.3567,8.7499,49.4371|Heilbronn:9.1638,49.113,9.2672,49.1766
   Paris:2.2241,48.8155,2.4699,48.9022
   ```

#### bcircles
Circle(s) defined by center coordinates and radius in meters.

**Formats**:
1. Simple: `lon,lat,radius|lon,lat,radius|...`
   ```
   8.6528,49.3683,1000|8.7294,49.4376,1000
   ```

2. Named: `id1:lon,lat,radius|id2:lon,lat,radius|...`
   ```
   Circle1:8.6528,49.3683,1000|Circle2:8.7294,49.4376,1000
   ```

#### bpolys
Polygon(s) as coordinate lists or GeoJSON FeatureCollection.

**Requirements**:
- First point must equal last point (closed polygon)
- MultiPolygons only supported in GeoJSON format

**Formats**:
1. Coordinate list:
   ```
   8.65821,49.41129,8.65821,49.41825,8.70053,49.41825,8.70053,49.41129,8.65821,49.41129
   ```

2. Named coordinate list:
   ```
   Region1:8.65821,49.41129,8.65821,49.41825,8.70053,49.41825,8.70053,49.41129,8.65821,49.41129
   ```

3. GeoJSON FeatureCollection:
   ```json
   {
     "type": "FeatureCollection",
     "features": [{
       "type": "Feature",
       "properties": {"id": "Region1"},
       "geometry": {
         "type": "Polygon",
         "coordinates": [[[8.65821,49.41129],[8.65821,49.41825],[8.70053,49.41825],[8.70053,49.41129],[8.65821,49.41129]]]
       }
     }]
   }
   ```


### Time Parameter
**Required for**: Extraction endpoints (`/elements/geometry`, `/elementsFullHistory`, `/contributions`)
**Optional for**: Aggregation endpoints (default: latest timestamp in OSHDB)

**Time Zone**: UTC only (Z suffix)

#### Supported Formats

1. **Single timestamp**: `2014-01-01` or `2014-01-01T12:30:00`
   
2. **List of timestamps**: `2014-01-01,2015-07-01,2018-10-10`

3. **Interval with period**: `2014-01-01/2018-01-01/P1Y`
   - Format: `start/end/period`
   - Period: `PnYnMnD` where n = size (e.g., `P1Y` = 1 year, `P6M` = 6 months, `P1M` = 1 month)

#### Timestamp Formats
- **Full**: `YYYY-MM-DD` or `YYYY-MM-DDThh:mm:ss`
- **Defaults**: 
  - Missing month/day: `01` is used
  - Missing time: `00:00:00Z` is used
  - Missing parameter: latest timestamp in OSHDB

#### Special Interval Notations
Using `#` to represent earliest/latest timestamps in OSHDB:

| Pattern | Meaning | Example |
|---------|---------|---------|
| `YYYY-MM-DD/YYYY-MM-DD` | start to end | `2013-01-01/2021-01-01` |
| `YYYY-MM-DD/YYYY-MM-DD/PnYnMnD` | start to end with period | `2013-01-01/2021-01-01/P2Y` |
| `/YYYY-MM-DD` | earliest # to end | `/2021-01-01` |
| `/YYYY-MM-DD/PnYnMnD` | earliest # to end with period | `/2021-01-01/P1Y` |
| `YYYY-MM-DD/` | start to latest # | `2013-01-01/` |
| `YYYY-MM-DD//PnYnMnD` | start to latest # with period | `2013-01-01//P1Y` |
| `/` | earliest # to latest # | `/` |
| `//PnYnMnD` | earliest # to latest # with period | `//P1Y` |

⚠️ **Note**: End timestamps are adjusted to align with start + multiples of period.
Example: `2010-01-01/2012-02-01/P1Y` → actual end becomes `2012-01-01`

### Filter Parameter (recommended, replaces deprecated types/keys/values)
**Combines**: OSM type + geometry type + OSM tags

⚠️ **Cannot combine** `filter` with deprecated `types`, `keys`, `values` parameters

#### Selectors

| Selector | Description | Example |
|----------|-------------|---------|
| `key=value` | Exact tag match | `natural=tree` |
| `key=*` | Any tag with given key | `addr:housenumber=*` |
| `key!=value` | Does not have exact tag | `oneway!=yes` |
| `key!=*` | Does not have any tag with key | `name!=*` |
| `key in (values)` | Key with one of given values | `highway in (residential, living_street)` |
| `type:osm-type` | OSM type (node/way/relation) | `type:node` |
| `id:osm-id` | Specific OSM ID¹ | `id:1234` |
| `id:type/id` | Specific OSM type+ID | `id:node/1234` |
| `id:(id-list)` | Multiple OSM IDs¹ | `id:(1, 42, 1234)` |
| `id:(type/id-list)` | Multiple type+IDs | `id:(node/1, way/3)` |
| `id:(range)` | ID range² | `id:(1..9999)` |
| `geometry:type` | Geometry type (point/line/polygon/other) | `geometry:polygon` |
| `area:(range)` | Area in m²² | `area:(1.0..1E6)` |
| `length:(range)` | Length in meters² | `length:(..100)` |
| `perimeter:(range)` | Perimeter in meters² | `perimeter:(..100)` |
| `geometry.vertices:(range)` | Number of points² | `geometry.vertices:(1..10)` |
| `geometry.outers:(range)` | Number of outer rings² | `geometry.outers:1` or `geometry.outers:(2..)` |
| `geometry.inners:(range)` | Number of holes (inner rings)² | `geometry.inners:0` or `geometry.inners:(1..)` |
| `geometry.roundness:(range)` | Roundness score²⁴ | `geometry.roundness:(0.8..)` |
| `geometry.squareness:(range)` | Squareness score²⁵ | `geometry.squareness:(0.8..)` |
| `changeset:id` | Specific changeset³ | `changeset:42` |
| `changeset:(id-list)` | Multiple changesets³ | `changeset:(10, 42)` |
| `changeset:(range)` | Changeset range³ | `changeset:(10..42)` |

**Notes**:
¹ OSM IDs are not unique between types. Use with type filter or combined `id:type/id` format.
² Range bounds can be omitted: `(10..)` = 10 or higher, `(..100)` = up to 100.
³ Changeset filters only work in contribution-based endpoints.
⁴ Roundness: Polsby-Popper test score (0-1, where 1 = perfect circle).
⁵ Squareness: Rectilinearity measurement by Žunić and Rosin (0-1, where 1 = perfect rectangle).

#### Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `(...)` | Grouping/precedence | `highway=primary and (name=* or ref=*)` |
| `not X` | Negation | `not type:node` |
| `X and Y` | Both conditions | `highway=service and service=driveway` |
| `X or Y` | Either condition | `natural=wood or landuse=forest` |

**Precedence**: Parentheses > `not` > `and` > `or`

#### Special Characters & Whitespace
- **Allowed unquoted**: `a-z`, `A-Z`, `0-9`, `_`, `-`, `:`
- **Requires quotes**: Any other characters
  - Example: `name="Heidelberger Brückenaffe"` or `opening_hours="24/7"`
- **Escape sequences**: `\"` for quote, `\\` for backslash
- **Whitespace**: Freely allowed between operators (`name = *` = `name=*`)

#### Common Filter Examples

| OSM Feature | Filter | Notes |
|-------------|--------|-------|
| Forests/woods | `(landuse=forest or natural=wood) and geometry:polygon` | Includes closed ways and multipolygons |
| Parks + benches | `leisure=park and geometry:polygon or amenity=bench and (geometry:point or geometry:line)` | Multiple geometry types |
| Buildings | `building=* and building!=no and geometry:polygon` | Excludes `building=no` tags |
| Highways | `type:way and (highway in (motorway, motorway_link, trunk, trunk_link, primary, primary_link, secondary, secondary_link, tertiary, tertiary_link, unclassified, residential, living_street, pedestrian) or (highway=service and service=alley))` | Adjust list per use case |
| Unnamed residential roads | `type:way and highway=residential and name!=* and noname!=yes` | Quality assurance filter |
| Large buildings | `geometry:polygon and building=* and building!=no and area:(1E6..)` | Area > 1M m² |


### Grouping Parameters

Used with `/groupBy/{groupType}` endpoints.

#### groupByKeys
- **Endpoint**: `/groupBy/key` only
- **Format**: Comma-separated list of OSM keys
- **Example**: `"building:roof,building:roof:colour"`
- **Result**: Separate results per key + remainder for unmatched objects
- **Note**: Elements can match 0, 1, or multiple keys → sum may exceed simple aggregation

#### groupByKey
- **Endpoint**: `/groupBy/tag` only
- **Format**: Single OSM key
- **Example**: `"highway"`
- **Mandatory**: Yes (no default)

#### groupByValues
- **Endpoint**: `/groupBy/tag` only  
- **Format**: Comma-separated list of OSM values
- **Example**: `"primary,secondary,tertiary"`
- **Default**: Empty (returns all values found in data)
- **Result**: Separate results per tag + remainder for unmatched

### Other Common Parameters
- **format**: `'json'` or `'csv'` (default: `'json'`)
- **showMetadata**: `'true'`, `'false'`, `'yes'`, `'no'` (default: `'false'`)
- **timeout**: Custom timeout in seconds (default: server setting, check `/metadata`)
- **contributionType**: `'creation'`, `'deletion'`, `'tagChange'`, `'geometryChange'` (can combine with commas)
- **properties**: `'tags'`, `'metadata'`, `'contributionTypes'` (comma-separated, for extraction endpoints)
- **clipGeometry**: `'true'` or `'false'` (default: `'true'`, for extraction endpoints)

### Deprecated Parameters (use filter instead)
⚠️ **Not recommended**: `types`, `keys`, `values`

---

## RESPONSE STRUCTURE

### General Response Parameters
Present in every response:

```json
{
  "attribution": {
    "url": "https://ohsome.org/copyrights",
    "text": "© OpenStreetMap contributors"
  },
  "apiVersion": "1.10.4",
  ...
}
```

### Aggregation Response Parameters

#### Standard Result
```json
{
  "result": [{
    "timestamp": "2021-01-01T00:00:00Z",  // for /elements, /users
    "value": 12345.0
  }]
}
```

#### Interval Result (contributions)
```json
{
  "result": [{
    "fromTimestamp": "2020-01-01T00:00:00Z",
    "toTimestamp": "2020-02-01T00:00:00Z",
    "value": 150.0
  }]
}
```

#### Ratio Result
```json
{
  "ratioResult": [{
    "timestamp": "2021-01-01T00:00:00Z",
    "value": 100000.0,    // numerator (filter)
    "value2": 25000.0,    // denominator (filter2)
    "ratio": 0.25         // value2/value
  }]
}
```

#### GroupBy Result
```json
{
  "groupByResult": [{
    "groupByObject": "amenity=restaurant",  // or boundary name, or "remainder"
    "result": [{
      "timestamp": "2021-01-01T00:00:00Z",
      "value": 5000.0
    }]
  }]
}
```

### Extraction Response Parameters

Responses are GeoJSON FeatureCollections with custom properties marked with `@`.

#### Common Extraction Properties
- `@osmId`: OSM element ID with type (e.g., `"node/1234"`)
- `@version`: Version number of OSM element
- `@changesetId`: Changeset ID that last modified this element
- `@osmType`: OSM element type (`"node"`, `"way"`, `"relation"`)

#### Elements Snapshot Properties
- `@snapshotTimestamp`: Timestamp of requested snapshot
- `@lastEdit`: When this feature was last edited

#### Elements Full History Properties
- `@validFrom`: When creation/change occurred (or `fromTimestamp` if before interval)
- `@validTo`: When feature stayed unchanged (or `toTimestamp` if after interval)

#### Contributions Properties
- `@timestamp`: When contribution occurred
- `@contributionChangesetId`: Changeset where contribution was performed
- `@creation`: `true` if element newly matches query (exclusive with other types)
- `@geometryChange`: `true` if geometry changed (can combine with `@tagChange`)
- `@tagChange`: `true` if tags changed (can combine with `@geometryChange`)
- `@deletion`: `true` if element no longer matches query (exclusive with other types)

**Notes**:
- Contribution type properties only appear when `true` (never `false`)
- `@contributionChangesetId` can differ from `@changesetId` (e.g., when only child nodes of a way move)
- OSM tags with keys starting with `@` are prefixed with another `@` (e.g., `@osmId` → `@@osmId`)

#### OSM Tags
When `properties=tags` is requested, OSM tags appear as individual GeoJSON properties.

### Metadata Response
```json
{
  "extractRegion": {
    "spatialExtent": {
      "type": "Polygon",
      "coordinates": [[[-180, -90], [180, -90], [180, 90], [-180, 90], [-180, -90]]]
    },
    "temporalExtent": {
      "fromTimestamp": "2007-10-08T00:00:00Z",
      "toTimestamp": "2020-02-12T23:00:00Z"
    },
    "replicationSequenceNumber": 65032
  },
  "timeout": 60
}
```

---

## HTTP STATUS CODES

### 2xx Success
- **200 OK**: Successful request
  - ⚠️ **Note**: Broken GeoJSON with error at end still returns 200

### 4xx Client Errors
- **400 Bad Request**: Invalid parameters, malformed request
  - Incorrect parameter format
  - Missing mandatory parameters
  - Unknown parameters
  - Duplicate parameters
  - Malformed GeoJSON
  - Invalid parameter values
- **404 Not Found**: Boundary or time outside OSHDB coverage
- **413 Payload Too Large**: Request exceeded timeout

### 5xx Server Errors
- **500 Internal Server Error**: Unexpected ohsome API error
  - Bugs
  - Missing keytables
  - Database access failure
- **503 Service Unavailable**: Cluster backend temporarily unavailable

---

## 1. ELEMENTS AGGREGATION

### 1.1 Basic Aggregation
**Endpoint**: `POST /elements/{aggregation}`

**Aggregation types**: `area`, `count`, `length`, `perimeter`

**Python Example**:
```python
import requests

URL = 'https://api.ohsome.org/v1/elements/count'
data = {
    "bboxes": "2.2241,48.8155,2.4699,48.9022",  # Paris bbox
    "time": "2021-01-01",
    "filter": "amenity=restaurant and type:node",
    "format": "json"
}
response = requests.post(URL, data=data)
result = response.json()
```

**Response Structure**:
```json
{
  "attribution": {...},
  "apiVersion": "1.10.4",
  "result": [{
    "timestamp": "2021-01-01T00:00:00Z",
    "value": 12345.0
  }]
}
```

### 1.2 Density
**Endpoint**: `POST /elements/{aggregation}/density`

Returns density per square kilometer.

**Python Example**:
```python
URL = 'https://api.ohsome.org/v1/elements/count/density'
data = {
    "bboxes": "2.2241,48.8155,2.4699,48.9022",
    "time": "2021-01-01",
    "filter": "amenity=cafe and type:node"
}
response = requests.post(URL, data=data)
```

### 1.3 Ratio
**Endpoint**: `POST /elements/{aggregation}/ratio`

Ratio of elements satisfying `filter2` to elements satisfying `filter`.

**Additional Parameters**:
- **filter2**: Second filter for ratio calculation

**Python Example**:
```python
URL = 'https://api.ohsome.org/v1/elements/length/ratio'
data = {
    "bboxes": "2.2241,48.8155,2.4699,48.9022",
    "time": "2015-01-01/2021-01-01/P2Y",
    "filter": "highway=residential and type:way",
    "filter2": "highway=residential and oneway=yes and type:way"
}
response = requests.post(URL, data=data)
```

**Response Structure**:
```json
{
  "ratioResult": [{
    "timestamp": "2015-01-01T00:00:00Z",
    "value": 100000.0,
    "value2": 25000.0,
    "ratio": 0.25
  }]
}
```

### 1.4 Group By
**Endpoint**: `POST /elements/{aggregation}/groupBy/{groupType}`

**Group types**: `boundary`, `key`, `tag`, `type`

**Additional Parameters**:
- **groupByKeys**: List of keys (for groupBy/key)
- **groupByKey**: Single key (for groupBy/tag)
- **groupByValues**: List of values (for groupBy/tag)

**Python Example - Group by Tag**:
```python
URL = 'https://api.ohsome.org/v1/elements/count/groupBy/tag'
data = {
    "bboxes": "2.2241,48.8155,2.4699,48.9022",
    "time": "2021-01-01",
    "filter": "amenity=* and type:node",
    "groupByKey": "amenity",
    "groupByValues": "restaurant,cafe,bar,pub"
}
response = requests.post(URL, data=data)
```

**Response Structure**:
```json
{
  "groupByResult": [
    {
      "groupByObject": "amenity=restaurant",
      "result": [{"timestamp": "2021-01-01T00:00:00Z", "value": 5000.0}]
    },
    {
      "groupByObject": "amenity=cafe",
      "result": [{"timestamp": "2021-01-01T00:00:00Z", "value": 3000.0}]
    }
  ]
}
```

**Python Example - Group by Boundary**:
```python
URL = 'https://api.ohsome.org/v1/elements/count/groupBy/boundary'
data = {
    "bboxes": "Area1:2.25,48.82,2.35,48.90|Area2:2.35,48.82,2.45,48.90",
    "time": "2021-01-01",
    "filter": "building=* and type:way"
}
response = requests.post(URL, data=data)
```

### 1.5 Density Group By
**Endpoint**: `POST /elements/{aggregation}/density/groupBy/{groupType}`

Combines density calculation with grouping.

### 1.6 Group By Boundary and Tag
**Endpoint**: `POST /elements/{aggregation}/groupBy/boundary/groupBy/tag`

Double grouping by both boundary and tag.

**Python Example**:
```python
URL = 'https://api.ohsome.org/v1/elements/length/groupBy/boundary/groupBy/tag'
data = {
    "bboxes": "Zone1:2.25,48.82,2.35,48.90|Zone2:2.35,48.82,2.45,48.90",
    "time": "2021-01-01",
    "filter": "highway=* and type:way",
    "groupByKey": "highway",
    "groupByValues": "primary,secondary,tertiary"
}
response = requests.post(URL, data=data)
```

---

## 2. USERS AGGREGATION

### 2.1 User Count
**Endpoint**: `POST /users/count`

Count unique users who contributed.

**Additional Parameter**:
- **contributionType**: Filter by contribution type
  - Values: `'creation'`, `'deletion'`, `'tagChange'`, `'geometryChange'`
  - Can combine multiple

**Python Example**:
```python
URL = 'https://api.ohsome.org/v1/users/count'
data = {
    "bboxes": "2.2241,48.8155,2.4699,48.9022",
    "time": "2020-01-01/2021-01-01/P1M",
    "filter": "building=* and type:way",
    "contributionType": "creation,geometryChange"
}
response = requests.post(URL, data=data)
```

**Response Structure**:
```json
{
  "result": [
    {
      "fromTimestamp": "2020-01-01T00:00:00Z",
      "toTimestamp": "2020-02-01T00:00:00Z",
      "value": 150.0
    }
  ]
}
```

### 2.2 User Count with Grouping
**Endpoints**:
- `POST /users/count/groupBy/{groupType}`
- `POST /users/count/density`
- `POST /users/count/density/groupBy/{groupType}`

Similar to elements aggregation grouping.

---

## 3. CONTRIBUTIONS AGGREGATION

### 3.1 Contributions Count
**Endpoint**: `POST /contributions/count`

**⚠️ Experimental Feature**: Subject to changes

**Additional Parameter**:
- **contributionType**: Same as users

**Python Example**:
```python
URL = 'https://api.ohsome.org/v1/contributions/count'
data = {
    "bboxes": "2.2241,48.8155,2.4699,48.9022",
    "time": "2020-01-01,2021-01-01",
    "filter": "building=residential and type:way",
    "contributionType": "creation"
}
response = requests.post(URL, data=data)
```

### 3.2 Latest Contributions
**Endpoints**:
- `POST /contributions/latest/count`
- `POST /contributions/latest/count/density`

Get only the latest contribution per entity in the time interval.

**Python Example**:
```python
URL = 'https://api.ohsome.org/v1/contributions/latest/count'
data = {
    "bboxes": "2.2241,48.8155,2.4699,48.9022",
    "time": "2020-01-01,2021-01-01",
    "filter": "shop=* and type:node",
    "contributionType": "tagChange"
}
response = requests.post(URL, data=data)
```

### 3.3 Contributions with Grouping
**Endpoints**:
- `POST /contributions/count/groupBy/boundary`
- `POST /contributions/count/density/groupBy/boundary`

---

## 4. ELEMENTS EXTRACTION

### 4.1 Extract Elements (GeoJSON)
**Endpoint**: `POST /elements/{geometryType}`

**Geometry types**: `geometry`, `bbox`, `centroid`

**Additional Parameters**:
- **properties**: `'tags'`, `'metadata'`, or both (comma-separated)
- **clipGeometry**: `'true'` or `'false'` (default: `'true'`)

**Python Example**:
```python
URL = 'https://api.ohsome.org/v1/elements/geometry'
data = {
    "bboxes": "2.2241,48.8155,2.4699,48.9022",
    "time": "2021-01-01",
    "filter": "amenity=restaurant and type:node",
    "properties": "tags,metadata",
    "clipGeometry": "true"
}
response = requests.post(URL, data=data)
geojson = response.json()
```

**Response**: GeoJSON FeatureCollection with OSM features

### 4.2 Full History Extraction
**Endpoint**: `POST /elementsFullHistory/{geometryType}`

Get all historical versions of matching features.

**Required**: `time` must be an interval (two timestamps)

**Python Example**:
```python
URL = 'https://api.ohsome.org/v1/elementsFullHistory/geometry'
data = {
    "bboxes": "2.3522,48.8566,2.3541,48.8578",  # Small area
    "time": "2015-01-01,2021-01-01",
    "filter": "historic=monument and type:way",
    "properties": "tags,metadata"
}
response = requests.post(URL, data=data)
```

**Response**: GeoJSON with `@validFrom` and `@validTo` properties

---

## 5. CONTRIBUTIONS EXTRACTION

### 5.1 Extract Contributions
**Endpoint**: `POST /contributions/{geometryType}`

Get all contributions (changes) as GeoJSON.

**Additional Parameters**:
- **properties**: `'tags'`, `'metadata'`, `'contributionTypes'`
- **clipGeometry**: Same as elements extraction

**Python Example**:
```python
URL = 'https://api.ohsome.org/v1/contributions/geometry'
data = {
    "bboxes": "2.2241,48.8155,2.4699,48.9022",
    "time": "2020-01-01,2021-01-01",
    "filter": "amenity=restaurant and type:node",
    "properties": "tags,metadata,contributionTypes",
    "contributionType": "creation,tagChange"
}
response = requests.post(URL, data=data)
```

**Response**: GeoJSON with contribution properties:
- `@changesetId`
- `@timestamp`
- `@version`
- `@creation`, `@deletion`, `@tagChange`, `@geometryChange` (booleans)

### 5.2 Latest Contributions Extract
**Endpoint**: `POST /contributions/latest/{geometryType}`

Get only the latest contribution per entity.

---

## 6. METADATA

### 6.1 Get API Metadata
**Endpoint**: `GET /metadata`

No parameters. Returns OSHDB coverage info.

**Python Example**:
```python
import requests
URL = 'https://api.ohsome.org/v1/metadata'
response = requests.get(URL)
metadata = response.json()
print(f"Data covers: {metadata['extractRegion']['temporalExtent']}")
```

---

## COMMON USE CASES FOR PARIS ANALYSIS

### Case 1: Count amenities over time
```python
import requests

URL = 'https://api.ohsome.org/v1/elements/count'
paris_bbox = "2.2241,48.8155,2.4699,48.9022"

data = {
    "bboxes": paris_bbox,
    "time": "2013-01-01/2021-01-01/P1Y",
    "filter": "amenity=cafe and type:node",
    "format": "json"
}
response = requests.post(URL, data=data)
results = response.json()['result']
```

### Case 2: Compare building density by area
```python
URL = 'https://api.ohsome.org/v1/elements/count/density/groupBy/boundary'

# Define multiple areas (e.g., arrondissements)
areas = "16th:2.24,48.84,2.29,48.88|18th:2.33,48.88,2.37,48.91"

data = {
    "bboxes": areas,
    "time": "2021-01-01",
    "filter": "building=* and type:way"
}
response = requests.post(URL, data=data)
```

### Case 3: Extract POIs with full attributes
```python
URL = 'https://api.ohsome.org/v1/elements/geometry'

data = {
    "bboxes": "2.2241,48.8155,2.4699,48.9022",
    "time": "2021-01-01",
    "filter": "shop=* and type:node",
    "properties": "tags,metadata"
}
response = requests.post(URL, data=data)
geojson = response.json()

# Process as GeoDataFrame
import geopandas as gpd
gdf = gpd.GeoDataFrame.from_features(geojson['features'])
```

### Case 4: Track mapping activity
```python
URL = 'https://api.ohsome.org/v1/users/count'

data = {
    "bboxes": "2.2241,48.8155,2.4699,48.9022",
    "time": "2013-01-01/2021-01-01/P1Y",
    "filter": "building=* and type:way",
    "contributionType": "creation"
}
response = requests.post(URL, data=data)
```

### Case 5: Analyze building changes
```python
URL = 'https://api.ohsome.org/v1/contributions/count'

data = {
    "bboxes": "2.2241,48.8155,2.4699,48.9022",
    "time": "2013-01-01,2021-01-01",
    "filter": "building=* and type:way",
    "contributionType": "creation,geometryChange"
}
response = requests.post(URL, data=data)
```

---

## FILTER SYNTAX GUIDE

### Basic Filters
- Tag exists: `"amenity=*"`
- Tag equals value: `"amenity=restaurant"`
- Multiple values (OR): `"highway in (primary,secondary,tertiary)"`
- Negation: `"building=* and building!=no"`

### Combining Filters
- AND: `"building=yes and building:levels>5"`
- OR: `"amenity=cafe or amenity=restaurant"`
- Parentheses: `"(amenity=cafe or amenity=bar) and wheelchair=yes"`

### Type Filters
- OSM type: `"type:node"`, `"type:way"`, `"type:relation"`
- Geometry type: `"geometry:point"`, `"geometry:line"`, `"geometry:polygon"`

### ID Filter
- Specific feature: `"id:way/140112810"`

---

## PRACTICAL EXAMPLES WITH PARIS DATA

## PRACTICAL EXAMPLES WITH PARIS DATA

### Example 1: Using GeoJSON Polygon for Paris Arrondissement
```python
import requests
import geopandas as gpd

# Load your IRIS/quartier polygon
gdf = gpd.read_file('iris_paris75.geojson')
quartier = gdf[gdf['nom_iris'].str.contains('Marais')].iloc[0]

# Convert to GeoJSON FeatureCollection for ohsome
import json
geojson_fc = {
    "type": "FeatureCollection",
    "features": [{
        "type": "Feature",
        "properties": {"id": "Marais"},
        "geometry": json.loads(quartier.geometry.to_json())
    }]
}

URL = 'https://api.ohsome.org/v1/elements/count'
data = {
    "bpolys": json.dumps(geojson_fc),
    "time": "2013-01-01/2021-01-01/P2Y",
    "filter": "amenity in (restaurant, cafe, bar) and type:node"
}
response = requests.post(URL, data=data)
results = response.json()
```

### Example 2: Group by Multiple Quartiers
```python
# Query multiple quartiers at once using bboxes
URL = 'https://api.ohsome.org/v1/elements/count/groupBy/boundary'

# Define bboxes for multiple quartiers
quartiers_bbox = (
    "Marais:2.355,48.855,2.365,48.865|"
    "Bastille:2.365,48.850,2.380,48.860|"
    "Montmartre:2.338,48.884,2.348,48.894"
)

data = {
    "bboxes": quartiers_bbox,
    "time": "2013-01-01/2021-01-01/P1Y",
    "filter": "shop=* and type:node"
}
response = requests.post(URL, data=data)
```

### Example 3: Amenity Evolution by Type
```python
URL = 'https://api.ohsome.org/v1/elements/count/groupBy/tag'

data = {
    "bboxes": "2.2241,48.8155,2.4699,48.9022",  # Paris
    "time": "2013-01-01/2021-01-01/P2Y",
    "filter": "amenity=* and type:node",
    "groupByKey": "amenity",
    "groupByValues": "restaurant,cafe,bar,fast_food,pub"
}
response = requests.post(URL, data=data)
results = response.json()

# Process results for temporal analysis
import pandas as pd
records = []
for group in results['groupByResult']:
    amenity_type = group['groupByObject']
    for res in group['result']:
        records.append({
            'amenity': amenity_type,
            'timestamp': res['timestamp'],
            'count': res['value']
        })
df = pd.DataFrame(records)
```

### Example 4: Extract POIs with Tags for Spatial Join
```python
URL = 'https://api.ohsome.org/v1/elements/geometry'

data = {
    "bboxes": "2.2241,48.8155,2.4699,48.9022",
    "time": "2021-01-01",
    "filter": "amenity in (restaurant, cafe, bar) and type:node",
    "properties": "tags"
}
response = requests.post(URL, data=data)
geojson = response.json()

# Convert to GeoDataFrame
gdf_pois = gpd.GeoDataFrame.from_features(geojson['features'], crs='EPSG:4326')

# Spatial join with IRIS quartiers
iris_gdf = gpd.read_file('iris_paris75.geojson')
joined = gpd.sjoin(gdf_pois, iris_gdf, how='left', predicate='within')

# Count POIs per quartier
poi_counts = joined.groupby('quartier_iris').size()
```

### Example 5: Track Building Changes Over Time
```python
URL = 'https://api.ohsome.org/v1/contributions/count'

data = {
    "bboxes": "2.2241,48.8155,2.4699,48.9022",
    "time": "2013-01-01,2021-01-01",
    "filter": "building=* and type:way",
    "contributionType": "creation,geometryChange"
}
response = requests.post(URL, data=data)
```

### Example 6: Compare Density Across Quartiers
```python
URL = 'https://api.ohsome.org/v1/elements/count/density/groupBy/boundary'

# Use named bboxes for quartiers
data = {
    "bboxes": "West:2.25,48.84,2.33,48.88|East:2.37,48.84,2.45,48.88",
    "time": "2021-01-01",
    "filter": "amenity=restaurant and type:node"
}
response = requests.post(URL, data=data)

# Results show density per km²
for group in response.json()['groupByResult']:
    print(f"{group['groupByObject']}: {group['result'][0]['value']:.2f} restaurants/km²")
```

### Example 7: Evolution Grouped by Boundary AND Tag
```python
URL = 'https://api.ohsome.org/v1/elements/count/groupBy/boundary/groupBy/tag'

data = {
    "bboxes": "16th:2.24,48.84,2.29,48.88|18th:2.33,48.88,2.37,48.91",
    "time": "2013-01-01/2021-01-01/P4Y",
    "filter": "shop=* and type:node",
    "groupByKey": "shop",
    "groupByValues": "bakery,butcher,convenience,supermarket"
}
response = requests.post(URL, data=data)

# Results grouped by BOTH boundary and shop type
for group in response.json()['groupByResult']:
    boundary, shop_type = group['groupByObject']
    print(f"{boundary} - {shop_type}:")
    for res in group['result']:
        print(f"  {res['timestamp']}: {res['value']}")
```

---

## ERROR HANDLING

```python
import requests

try:
    response = requests.post(URL, data=data, timeout=300)
    response.raise_for_status()  # Raise exception for HTTP errors
    result = response.json()
except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
```

---

## BEST PRACTICES

1. **Use appropriate aggregation endpoints** for large areas (faster than extraction)
2. **Set reasonable timeouts** for complex queries
3. **Use filter parameter** instead of deprecated types/keys/values
4. **Request only needed properties** in extraction endpoints
5. **Use groupBy/boundary** for spatial comparisons
6. **Cache results** when possible to reduce API load
7. **Use time intervals** with appropriate granularity (P1Y for yearly, P1M for monthly)

---

## RATE LIMITS & PERFORMANCE

- Default timeout: Check via `/metadata` endpoint
- Custom timeout: Use `timeout` parameter
- Large queries: Consider breaking into smaller spatial/temporal chunks
- GeoJSON extraction: Most resource-intensive, use sparingly

---

## ATTRIBUTION

Always include in publications:
```
© OpenStreetMap contributors
URL: https://ohsome.org/copyrights
```
