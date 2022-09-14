fn main() {
    cxx_build::bridge("src/qbjs_deserializer.rs")
        .flag_if_supported("-std=c++17")
        .compile("qbjs_deserialize_cxx");

    println!("cargo:rerun-if-changed=src/lib.rs");
}
