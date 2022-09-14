pub use anyhow::Result;
pub use cxx::CxxVector;
pub use qbjs_deserializer::qbjs;
use qbjs_deserializer::qbjs::DeserializeError;

#[cxx::bridge]
pub mod ffi {
    #[namespace = "qbjs_deserializer"]
    extern "Rust" {
        fn deserialize_to_json(data: &CxxVector<u8>) -> Result<String>;
    }
}

fn deserialize_error_message(deserialize_error: &DeserializeError) -> String {
    let error_message = match deserialize_error {
        DeserializeError::InsufficientData => "Not enough data to analyze (slice too small)",
        DeserializeError::InvalidRootContainer => "Root value isn't an object or an array (invalid root container)",
        DeserializeError::AnalysisError(analysis_error) => match analysis_error {
            qbjs::analysis::AnalysisError::HeaderAnalysisError(header_error) => {
                match header_error {
                    qbjs::analysis::header::Error::InvalidLength => "Invalid QBJS header length",
                    qbjs::analysis::header::Error::InvalidTag => "Invalid QBJS header tag",
                    qbjs::analysis::header::Error::InvalidVersion => "Invalid QBJS header version",
                }
            }

            qbjs::analysis::AnalysisError::MetadataAnalysisError(metadata_error) => {
                match metadata_error {
                    qbjs::analysis::metadata::Error::InvalidContainerBaseLength => {
                        "Attempted to read an array or an object but reached end of slice"
                    }
                    qbjs::analysis::metadata::Error::InvalidValueHeaderSize => {
                        "Attempted to read a value header but reached end of slice"
                    }
                }
            }
            qbjs::analysis::AnalysisError::DataAnalysisError(data_error) => match data_error {
                qbjs::analysis::data::Error::UnknownQtValue => "Unknown Qt value (doesn't match QJsonValue::ValueType enum)",
                qbjs::analysis::data::Error::InvalidValueLength => "Attempted to read some data but reached end of slice",
                qbjs::analysis::data::Error::InvalidArrayContainer => "Attempted to read an array (indicated by value header) but container has the object flag set",
                qbjs::analysis::data::Error::InvalidObjectContainer => "Attempted to read an object (indicated by value header) but container doesn't have the object flag set",
            },
        },
        DeserializeError::ReadError(read_error) => match read_error {
            qbjs::read::ReadError::FailedToDecodeLatin1String => "Failed to decode Latin 1 string (key or value)",
            qbjs::read::ReadError::FailedToDecodeUtf16String => "Failed to decode UTF-16 string (key or value)",
            qbjs::read::ReadError::InvalidBoolDataPosition => "Attempted to read a bool value but reached end of slice",
            qbjs::read::ReadError::InvalidSelfContainedNumberDataPosition => "Attempted to read a (self-container) number value but reached end of slice",
            qbjs::read::ReadError::InvalidNumberDataRange => "Attempted to read a number value but reached end of slice",
            qbjs::read::ReadError::InvalidLatin1StringDataRange => "Attempted to read a Latin 1 string (key or value) but reached end of slice",
            qbjs::read::ReadError::InvalidUtf16StringDataRange => "Attempted to read a UTF-16 string (key or value) but reached end of slice",
        }
    };
    error_message.to_owned()
}

fn deserialize_to_json(data: &CxxVector<u8>) -> anyhow::Result<String> {
    match qbjs::deserialize_to_json(data.as_slice()) {
        Ok(value) => Ok(value.to_string()),
        Err(e) => Err(anyhow::Error::msg(deserialize_error_message(&e))),
    }
}
