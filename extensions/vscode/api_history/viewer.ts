import * as fs from 'fs';
import * as msgpack from 'msgpack-lite';

// Function to read and decode a MessagePack file
const readMessagePackFile = (filePath: string) => {
    try {
        // Read the packed data from the file
        const packedData = fs.readFileSync(filePath);
        
        // Decode the packed data to a JavaScript object
        const decodedData = msgpack.decode(packedData);
        
        // Convert the object to a human-readable JSON format
        const jsonString = JSON.stringify(decodedData, null, 2); 
        
        // Save the JSON string to a file in the same directory
        const outputFilePath = './history.json'; 
        fs.writeFileSync(outputFilePath, jsonString, { encoding: 'utf8' });
        
        console.log(`Decoded data saved to ${outputFilePath}`);
    } catch (error) {
        console.error(`Error reading or decoding the file: ${error.message}`);
    }
};

// Specify the path to your MessagePack file
const filePath = './history.msgpack'; 
readMessagePackFile(filePath);