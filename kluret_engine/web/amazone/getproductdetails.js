async function updateJsonFile() {
    // Function to generate a random alphanumeric string of given length
    function generateRandomID(length) {
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        let result = '';
        for (let i = 0; i < length; i++) {
            result += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        return result;
    }

    try {
        // Get the current page URL
        const currentPageUrl = window.location.href;

        // Extract product title
        const productTitleElement = document.querySelector('#productTitle');
        const productTitle = productTitleElement ? productTitleElement.innerText.trim() : '';

        // Extract product price
        const priceElement = document.querySelector('.priceToPay .a-price-whole');
        const priceFractionElement = document.querySelector('.priceToPay .a-price-fraction');
        const priceSymbolElement = document.querySelector('.priceToPay .a-price-symbol');
        const productPrice = getPrice(priceElement, priceFractionElement, priceSymbolElement);

        // Extract product images
        const imageElements = document.querySelectorAll('#altImages .a-button-thumbnail img'); // Updated selector
        const imageLinks = Array.from(imageElements).map(img => img.src);

        // Extract technical information
        const techInfoRows = document.querySelectorAll('.content-grid-block table.a-bordered tbody tr');
        let technicalInformation = {};
        techInfoRows.forEach(row => {
            const keyElement = row.querySelector('td:nth-child(1) p strong');
            const valueElement = row.querySelector('td:nth-child(2) p');
            if (keyElement && valueElement) {
                const key = keyElement.innerText.trim();
                const value = valueElement.innerText.trim();
                technicalInformation[key] = value;
            }
        });

        // New product data including current product URL
        let newProductData = {
            "productID": generateRandomID(Math.floor(Math.random() * (70 - 20 + 1)) + 20),
            "title": productTitle,
            "price": productPrice,
            "technicalInformation": technicalInformation,
            "imageLinks": imageLinks,
            "P_URL": currentPageUrl // Add the current page URL here
        };

        // Output the new product data
        console.log(JSON.stringify(newProductData, null, 2));

        // Here you can proceed with saving this data to a JSON file or further processing
        // For demonstration purposes, we output the JSON data to console

    } catch (err) {
        console.error('Error:', err);
    }
}

// Function to get formatted price
function getPrice(element1, element2, element3) {
    const priceElement = element1 ? element1.innerText.trim() : '';
    const priceFractionElement = element2 ? element2.innerText.trim() : '';
    const priceSymbolElement = element3 ? element3.innerText.trim() : '';
    return `${priceElement}${priceFractionElement}${priceSymbolElement}`.trim();
}

// Run the function to update the JSON file
updateJsonFile();

// Add event listener for Enter key press
document.addEventListener('keydown', async function(event) {
    if (event.key === 'alt') {
        await updateJsonFile();
    }
});
