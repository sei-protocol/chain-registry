package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
)

type Asset struct {
	Name        string            `json:"name"`
	Description string            `json:"description"`
	Symbol      string            `json:"symbol"`
	Base        string            `json:"base"`
	Display     string            `json:"display"`
	DenomUnits  []DenomUnit       `json:"denom_units"`
	Images      map[string]string `json:"images"`
}

type DenomUnit struct {
	Denom    string `json:"denom"`
	Exponent int    `json:"exponent"`
}

// TODO: Make this configurable
const Pacific1GRPC = "gprc.pacific-1.seinetwork.io"
const Atlantic2GRPC = "grpc.atlantic-2.seinetwork.io"

func main() {
	file, err := ioutil.ReadFile("./schema/assetlist.json")
	if err != nil {
		fmt.Println("Failed to read file:", err)
		os.Exit(1)
	}

	var assets map[string][]Asset
	err = json.Unmarshal(file, &assets)
	if err != nil {
		fmt.Println("Failed to unmarshal JSON:", err)
		os.Exit(1)
	}

	// Verify Pacific-1 and Atlantic-2 Exists
	// TODO: Make this more configurable for more chains
	if _, exists := assets["pacific-1"]; !exists {
		fmt.Println("`pacific-1` key is missing in assetlist.json")
		os.Exit(1)
	}
	if _, exists := assets["atlantic-2"]; !exists {
		fmt.Println("`pacific-1` key is missing in assetlist.json")
		os.Exit(1)
	}

	fmt.Println("Validation successful!")
}
