#### ***deserialize(data)***

Deserialize the given data (that was serialized using `serialize()`) using
base64 encoding and pickle.

##### Parameters

- `data`: data to deserialize (must be serialized with base64 and pickle)

##### Returns

Deserialized data

---

#### ***serialize(data)***

Serialize the given data using base64 encoding and pickle.

##### Parameters

- `data`: data to serialize (must be picklable)

##### Returns

Serialized data string
