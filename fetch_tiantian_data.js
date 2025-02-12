// Import required modules
const axios = require('axios');
const fs = require('fs');

// Fetch historical data for the fund
async function fetchFundData(fundCode) {
    const url = `https://api.doctorxiong.club/v1/fund/detail?code=${fundCode}`;
    try {
        const response = await axios.get(url, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        });
        console.log('API Response:', response.data); // Log the full API response for debugging

        const data = response.data;

        if (!data || !data.data || !data.data.netWorthData) {
            throw new Error('No data found for the specified fund code.');
        }

        // Extract historical data
        const historicalData = data.data.netWorthData.map(entry => ({
            date: entry[0],
            netWorth: entry[1]
        }));

        console.log('Historical data fetched:', historicalData.slice(0, 5)); // Log first 5 entries for verification

        // Save data to a JSON file
        const filePath = './fund_006479.json';
        fs.writeFileSync(filePath, JSON.stringify(historicalData, null, 2));
        console.log(`Fund data saved to ${filePath}`);
    } catch (error) {
        console.error('Error fetching fund data:', error.message);
    }
}

// Main function
const fundCode = '006479'; // Fund code
fetchFundData(fundCode);