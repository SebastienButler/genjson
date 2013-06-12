/**
 * @file   main.cc
 * @author Sébastien Butler <sebastien.butler@gmail.com>
 * @date   Wed Apr 10 22:15:41 2013
 *
 * @brief  basic test main
 *
 *
 */
#include <json/json.h>
#include <iostream>
#include <fstream>
#include <string>
#include <memory>

#include "include/gen_parser.hh"
#include "include/gen_json_product.hh"

std::string readInputTestFile(const char* path)
{
  FILE* file = fopen(path, "rb");
  if (!file)
    return std::string("");
  fseek(file, 0, SEEK_END);
  long size = ftell(file);
  fseek(file, 0, SEEK_SET);
  std::string text;
  char* buffer = new char[size + 1];
  buffer[size] = 0;
  if (fread(buffer, 1, size, file) == (unsigned long)size)
    text = buffer;
  fclose(file);
  delete[] buffer;
  return text;
}

int main(int argc, char** argv)
{
  if (argc < 2)
  {
    return 1;
  }

  Json::Reader reader;
  Json::Value root;
  bool isOk = reader.parse(readInputTestFile(argv[1]), root);
  if (!isOk)
    std::cerr << reader.getFormatedErrorMessages() << std::endl;
  genjson::Parser parser;
  try
  {
    genjson::JsonObject* obj = parser(root)))
    if (genjson::JsonProduct* prod = dynamic_cast<genjson::JsonProduct*>(obj))
    {
      std::cout << "\"name\": " << prod->getName() << ",\n"
		<< "\"price\": " << prod->getPrice() << ",\n";
      std::shared_ptr<genjson::Jsonstock> stock = prod->getStock();
      std::cout << "\"stock\": \n\t\"warehouse\": " << stock->getWarehouse() << ",\n\t"
		<< "\"retail\":" << stock->getRetail() << "\n";
    }
    else if (genjson::JsonLol* lol = dynamic_cast<genjson::JsonLol*>(obj))
    {
      std::cout << "From: " << lol->getFrom() << "  To: " << lol->getTo()
		<< " with a power level of " << lol->getLevel()
		<< std::endl;
    }
  }
  catch (const std::exception& e)
  {
    std::cout << e.what() << std::endl;
  }
}
