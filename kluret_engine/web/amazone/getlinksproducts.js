async function scrapeAndDownloadUrls() {
    try {
        // Select all href URLs from the current page
        const urlElements = document.querySelectorAll('a.a-link-normal.s-no-outline');
        const urls = Array.from(urlElements).map(a => a.href);

        // Create a Blob containing the JSON data
        const jsonData = JSON.stringify(urls, null, 2);
        const blob = new Blob([jsonData], { type: 'application/json' });

        // Create a temporary URL for the Blob
        const url = URL.createObjectURL(blob);

        // Create an anchor element for download
        const downloadLink = document.createElement('a');
        downloadLink.href = url;
        downloadLink.download = 'Amazon_Product_URLs.json';

        // Append the anchor element to the body
        document.body.appendChild(downloadLink);

        // Programmatically trigger the download
        downloadLink.click();

        // Clean up: remove the anchor element and revoke the URL object
        downloadLink.remove();
        URL.revokeObjectURL(url);

        console.log('URLs have been downloaded as Amazon_Product_URLs.json');
    } catch (error) {
        console.error('Error:', error);
    }
}

// Run the function to scrape and download URLs
scrapeAndDownloadUrls();
