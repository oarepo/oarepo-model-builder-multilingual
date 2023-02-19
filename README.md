# OARepo Model Builder Multilingual

plugin for the [oarepo-model-builder module](https://github.com/oarepo/oarepo-model-builder) that adds support for
multilingual data types

## Usage

Within this plugin, two data types are added: multilingual and i18nstr. They can be added to the data model
using `type: multilingual` or `type: i18nstr`.
Values containing language tags must be in IETF [format](https://www.w3.org/International/articles/language-tags/).
The structure of both data types can be changed using the `multilingual` field

## i18nStr

An object that contains the language of the item and the actual value of the item.

### Example

#### Model

```json
"abstract": {"type": "i18nStr"}
```

#### Generated JsonSchema

```json
 "abstract": {
    "type": "object",
    "properties": {
        "lang": {
        "type": "string"
        },
        "value": {
        "type": "string"
        }
    }
  }
```

## Multilingual
Array of i18nStr objects.

### Example

#### Model

```json
"abstract": {"type": "multilingual"}
```

#### Generated Schema

```json
 "abstract": {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "lang": {
            "type": "string"
            },
            "value": {
            "type": "string"
            }
        }
    }
}
```

### Usage of i18nStr within another object
i18nstr can be added to another object using `"use": "i18n"`.
#### Example

### Supported languages:
Supported languages are defined in the object in the structure: `"supported language tag": {object containing additional
information}` within the field `supported-langs` in model settings.
Supported languages definition is used to specify the languages to be indexed in elasticsearch and opensearch,
respectively. All supplied data for the supported language will be inserted into the mapping definition.
#### Example
##### Model
```json
"model": {"properties": {"a": {"type": "multilingual"}}
          "settings": {"supported-langs": {
            "cs": {
                "text": {
                    "analyzer": "czech",
                },
                "sort": {
                    "type": "icu_collation_keyword"
                },
                "keyword": {
                    "test": "test"
                }
            },
            "en": {
                "text": {
                    "analyzer": "en"
                },
                "sort": {
                    "type": "icu_collation_keyword"
                }
            }}}}
```
##### Generated Schema
```json
"mappings": {
        "properties": {
            "a": {
                "type": "object",
                "properties": {
                    "lang": {
                        "type": "keyword"
                    },
                    "value": {
                        "type": "text"
                    }
                }
            },
            "a_cs": {
                "type": "text",
                "analyzer": "czech",
                "sort": {
                    "type": "icu_collation_keyword",
                    "index": false,
                    "language": "cs"
                },
                "fields": {
                    "keyword": {
                        "test": "test",
                        "type": "keyword"
                    }
                }
            },
            "a_en": {
                "type": "text",
                "analyzer": "en",
                "sort": {
                    "type": "icu_collation_keyword",
                    "index": false,
                    "language": "en"
                },
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                }
            }
}
```
### The change of the name of a language or value field
The name of the field for the language value and the name of the field for the value of the item itself can be changed
using the `multilingual` field and the `value-field` and `lang-field` fields. It is not required to rename both fields.
#### Example:
##### Model
```json
"b":{"type": "i18nStr", "multilingual":{"lang-field": "language", "value-field": "val"}}
```
##### Generated Schema
```python
class BSchema(ma.Schema, ):
    """BSchema schema."""
    
    language = ma_fields.String()
    
    val = ma_fields.String()
    
class TestSchema(ma.Schema, ):
    """TestSchema schema."""
    
    b = ma_fields.Nested(lambda: BSchema())

```
### Indexing another data type using supported languages
If supported languages are defined, indexing for these languages can be added to data types other than multilingual and
i18nStr. For this purpose you need to add to the field: `'multilingual': {'i18n': True}`
#### Example:
##### Model:
```json
"model": {"properties": {"a": {"type": "fulltext", "multilingual": {"i18n": true}}}
        "settings": {"supported-langs": {"cs": {}, "en": {}}}}
```
##### Schema:
```json
{"mappings":
{"properties":{
  "a":{"type":"text"},
  "a_cs":{"type":"text","fields":{"keyword":{"type":"keyword","ignore_above":50}}},
  "a_en":{"type":"text","fields":{"keyword":{"type":"keyword","ignore_above":50}}}}}}
```