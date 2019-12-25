#pragma once

#include <regex>
#include <tiny_gltf.h>

namespace tf2decomp {

	using namespace tinygltf;

	// Error code -1 -> couldn't open file

	std::string readfile(char* file, uint32_t* result) {
		FILE* fileptr = fopen(file, "r");
		if (fileptr == nullptr) {
			*result = -1;
			return "";
		}
		fseek(fileptr, 0, SEEK_END);
		uint64_t length = ftell(fileptr);
		fseek(fileptr, 0, SEEK_SET);
		std::string str;
		str.reserve(length);
		fread(&str[0], 1, length, fileptr);
		return str;
	}

	Model convertFromMemory(std::string content, uint32_t* result) {

	}

	Model convertFromFile(char* file, uint32_t* result) {
		std::string content = readfile(file, result);
		if (content.empty())
			return Model();
		return convertFromMemory(content, result);
	}
}
