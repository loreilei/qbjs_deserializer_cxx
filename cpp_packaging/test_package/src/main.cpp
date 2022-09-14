#include <qbjs_deserializer/qbjs_deserializer.hpp>

#include <cstring>
#include <exception>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

std::vector<uint8_t> load_file(std::string const& filepath) {
  std::ifstream ifs(filepath, std::ios::binary | std::ios::ate);

  if (!ifs) throw std::runtime_error(filepath + ": " + std::strerror(errno));

  auto end = ifs.tellg();
  ifs.seekg(0, std::ios::beg);

  auto size = std::size_t(end - ifs.tellg());

  if (size == 0) return {};

  std::vector<uint8_t> buffer(size);

  if (!ifs.read((char*)buffer.data(), buffer.size()))
    throw std::runtime_error(filepath + ": " + std::strerror(errno));

  return buffer;
}

int main(int argc, char** argv) {
  if (argc != 5) {
    std::cerr
        << "Not enough parameters" << std::endl
        << "Usage: 'testApp <path to qbjs file to read> <path to json file to "
           "write> <path to qbjs file with invalid header to read> <path to "
           "text file to write exception message>'"
        << std::endl;
    return -1;
  }

  // Test valid Qbjs file reading
  const std::string qbjsFilename(argv[1]);
  const std::string outputJsonFilename(argv[2]);

  try {
    const auto qbjsFileContent = load_file(qbjsFilename);
    const auto jsonContent =
        qbjs_deserializer::deserialize_to_json(qbjsFileContent);

    std::ofstream outputJsonFile(outputJsonFilename);

    if (!outputJsonFile) {
      throw std::runtime_error(outputJsonFilename + ": " +
                               std::strerror(errno));
    }

    outputJsonFile << std::string(jsonContent) << std::endl;
    outputJsonFile.close();
  } catch (const std::exception& e) {
    std::cerr << e.what() << std::endl;
    return -1;
  }

  // Test invalid header exception
  const std::string invalidHeaderQbjsFilename(argv[3]);
  const std::string outputTextFilename(argv[4]);

  try {
    const auto invalidHeaderQbjsFileContent =
        load_file(invalidHeaderQbjsFilename);
    const auto jsonContent =
        qbjs_deserializer::deserialize_to_json(invalidHeaderQbjsFileContent);

    // Should never be reached as we try to trigger an invalid qbjs header
    // exception
    std::cout << std::string(jsonContent) << std::endl;
  } catch (const std::exception& e) {
    std::ofstream outputTextFile(outputTextFilename);

    if (!outputTextFile) {
      std::cerr << outputTextFilename << ": " << std::strerror(errno);
      return -1;
    }

    outputTextFile << std::string(e.what()) << std::endl;
    outputTextFile.close();
  }

  return 0;
}
