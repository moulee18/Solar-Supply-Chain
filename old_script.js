// Sample dataset
const solarProducts = [
    {
        State: "California",
        City: "Los Angeles",
        "Product Name": "Renogy 400W Solar Panel",
        Price: "$299.99",
        Company: "Renogy",
        Location: "Los Angeles, CA",
        Rating: 4.8,
        Reviews: 1245,
        "Product Link": "https://example.com/product1",
        Category: "solar panel"
    },
    {
        State: "Texas",
        City: "Houston",
        "Product Name": "Eastron Energy Meter SDM630",
        Price: "$189.50",
        Company: "Eastron",
        Location: "Houston, TX",
        Rating: 4.6,
        Reviews: 892,
        "Product Link": "https://example.com/product2",
        Category: "energy meter"
    },
    {
        State: "Florida",
        City: "Miami",
        "Product Name": "6-String Solar Combiner Box",
        Price: "$145.00",
        Company: "MidNite Solar",
        Location: "Miami, FL",
        Rating: 4.7,
        Reviews: 634,
        "Product Link": "https://example.com/product3",
        Category: "combiner and fuse boxes"
    },
    {
        State: "California",
        City: "San Diego",
        "Product Name": "Type 2 Surge Protection Device",
        Price: "$225.00",
        Company: "Phoenix Contact",
        Location: "San Diego, CA",
        Rating: 4.9,
        Reviews: 1567,
        "Product Link": "https://example.com/product4",
        Category: "surge protection devices"
    },
    {
        State: "New York",
        City: "New York",
        "Product Name": "SolarEdge Data Logger",
        Price: "$320.00",
        Company: "SolarEdge",
        Location: "New York, NY",
        Rating: 4.5,
        Reviews: 723,
        "Product Link": "https://example.com/product5",
        Category: "data logger"
    },
    {
        State: "Arizona",
        City: "Phoenix",
        "Product Name": "10AWG DC Solar Cable 500ft",
        Price: "$175.00",
        Company: "WindyNation",
        Location: "Phoenix, AZ",
        Rating: 4.4,
        Reviews: 456,
        "Product Link": "https://example.com/product6",
        Category: "dc cables"
    },
    {
        State: "Texas",
        City: "Austin",
        "Product Name": "Growatt 5000W Inverter",
        Price: "$899.00",
        Company: "Growatt",
        Location: "Austin, TX",
        Rating: 4.7,
        Reviews: 1834,
        "Product Link": "https://example.com/product7",
        Category: "inverters"
    },
    {
        State: "California",
        City: "Sacramento",
        "Product Name": "Solar Monitoring System Pro",
        Price: "$450.00",
        Company: "Enphase",
        Location: "Sacramento, CA",
        Rating: 4.6,
        Reviews: 991,
        "Product Link": "https://example.com/product8",
        Category: "solar monitoring system"
    },
    {
        State: "Nevada",
        City: "Las Vegas",
        "Product Name": "Pyranometer Solar Sensor",
        Price: "$280.00",
        Company: "Kipp & Zonen",
        Location: "Las Vegas, NV",
        Rating: 4.8,
        Reviews: 512,
        "Product Link": "https://example.com/product9",
        Category: "solar sensor"
    },
    {
        State: "Florida",
        City: "Tampa",
        "Product Name": "Dual-Axis Solar Tracker",
        Price: "$1,299.00",
        Company: "AllEarth",
        Location: "Tampa, FL",
        Rating: 4.5,
        Reviews: 367,
        "Product Link": "https://example.com/product10",
        Category: "solar tracker"
    },
    {
        State: "Colorado",
        City: "Denver",
        "Product Name": "Digital Solar Tester Kit",
        Price: "$195.00",
        Company: "Fluke",
        Location: "Denver, CO",
        Rating: 4.9,
        Reviews: 1423,
        "Product Link": "https://example.com/product11",
        Category: "solar tester"
    }
];

const categories = [
    { name: 'All Products', value: 'all' },
    { name: 'Solar Panel', value: 'solar panel' },
    { name: 'Energy Meter', value: 'energy meter' },
    { name: 'Combiner & Fuse Boxes', value: 'combiner and fuse boxes' },
    { name: 'Surge Protection Devices', value: 'surge protection devices' },
    { name: 'Data Logger', value: 'data logger' },
    { name: 'DC Cables', value: 'dc cables' },
    { name: 'Inverters', value: 'inverters' },
    { name: 'Monitoring System', value: 'solar monitoring system' },
    { name: 'Solar Sensor', value: 'solar sensor' },
    { name: 'Solar Tracker', value: 'solar tracker' },
    { name: 'Solar Tester', value: 'solar tester' }
];

// State variables
let searchTerm = '';
let selectedCategory = 'all';
let selectedState = 'all';
let minRating = 0;
let sortBy = 'rating';

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    initializeCategoryButtons();
    initializeStateSelect();
    initializeEventListeners();
    renderProducts();
});

// Initialize category buttons
function initializeCategoryButtons() {
    const container = document.getElementById('categoryButtons');
    categories.forEach(cat => {
        const button = document.createElement('button');
        button.className = 'category-btn';
        if (cat.value === 'all') {
            button.classList.add('active');
        }
        button.textContent = cat.name;
        button.onclick = () => selectCategory(cat.value);
        container.appendChild(button);
    });
}

// Initialize state select dropdown
function initializeStateSelect() {
    const select = document.getElementById('stateSelect');
    const states = ['all', ...new Set(solarProducts.map(p => p.State))].sort();
    
    states.forEach(state => {
        const option = document.createElement('option');
        option.value = state;
        option.textContent = state === 'all' ? 'All States' : state;
        select.appendChild(option);
    });
}

// Initialize event listeners
function initializeEventListeners() {
    document.getElementById('searchInput').addEventListener('input', (e) => {
        searchTerm = e.target.value;
        renderProducts();
    });

    document.getElementById('stateSelect').addEventListener('change', (e) => {
        selectedState = e.target.value;
        renderProducts();
    });

    document.getElementById('ratingSlider').addEventListener('input', (e) => {
        minRating = parseFloat(e.target.value);
        document.getElementById('ratingValue').textContent = `${minRating}+ ⭐`;
        renderProducts();
    });

    document.getElementById('sortSelect').addEventListener('change', (e) => {
        sortBy = e.target.value;
        renderProducts();
    });
}

// Select category
function selectCategory(category) {
    selectedCategory = category;
    
    // Update active button
    const buttons = document.querySelectorAll('.category-btn');
    buttons.forEach(btn => {
        if (btn.textContent === categories.find(c => c.value === category).name) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
    
    renderProducts();
}

// Filter and sort products
function getFilteredProducts() {
    let filtered = solarProducts.filter(product => {
        const matchesSearch = product["Product Name"].toLowerCase().includes(searchTerm.toLowerCase()) ||
                            product.Company.toLowerCase().includes(searchTerm.toLowerCase()) ||
                            product.Category.toLowerCase().includes(searchTerm.toLowerCase());
        const matchesCategory = selectedCategory === 'all' || product.Category === selectedCategory;
        const matchesState = selectedState === 'all' || product.State === selectedState;
        const matchesRating = product.Rating >= minRating;
        
        return matchesSearch && matchesCategory && matchesState && matchesRating;
    });

    // Sort products
    filtered.sort((a, b) => {
        if (sortBy === 'rating') return b.Rating - a.Rating;
        if (sortBy === 'reviews') return b.Reviews - a.Reviews;
        if (sortBy === 'price') {
            const priceA = parseFloat(a.Price.replace(/[$,]/g, ''));
            const priceB = parseFloat(b.Price.replace(/[$,]/g, ''));
            return priceA - priceB;
        }
        return 0;
    });

    return filtered;
}

// Render stars
function renderStars(rating) {
    let starsHTML = '<div class="stars">';
    for (let i = 0; i < 5; i++) {
        if (i < Math.floor(rating)) {
            starsHTML += `
                <svg class="star star-filled" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
                </svg>
            `;
        } else {
            starsHTML += `
                <svg class="star star-empty" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
                </svg>
            `;
        }
    }
    starsHTML += `<span class="rating-score">${rating}</span>`;
    starsHTML += '</div>';
    return starsHTML;
}

// Render products
function renderProducts() {
    const container = document.getElementById('productsContainer');
    const filteredProducts = getFilteredProducts();
    
    // Update count
    document.getElementById('productCount').textContent = filteredProducts.length;

    if (filteredProducts.length === 0) {
        container.innerHTML = `
            <div class="empty-state" style="grid-column: 1 / -1;">
                <svg class="empty-icon" xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="16.5" x2="7.5" y1="9.4" y2="4.21"></line>
                    <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
                    <polyline points="3.29 7 12 12 20.71 7"></polyline>
                    <line x1="12" x2="12" y1="22" y2="12"></line>
                </svg>
                <h3>No products found</h3>
                <p>Try adjusting your filters or search terms</p>
            </div>
        `;
        return;
    }

    container.innerHTML = filteredProducts.map(product => `
        <div class="product-card">
            <div class="product-header-line"></div>
            <div class="product-content">
                <div>
                    <h3 class="product-name">${product["Product Name"]}</h3>
                    <p class="product-company">${product.Company}</p>
                </div>

                <div class="product-price">${product.Price}</div>

                <div class="product-rating">
                    ${renderStars(product.Rating)}
                    <span class="product-reviews">(${product.Reviews.toLocaleString()} reviews)</span>
                </div>

                <div class="product-location">
                    <svg class="location-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"></path>
                        <circle cx="12" cy="10" r="3"></circle>
                    </svg>
                    <span>${product.Location}</span>
                </div>

                <div class="product-category">
                    <span class="category-badge">${product.Category}</span>
                </div>

                <a href="${product["Product Link"]}" target="_blank" rel="noopener noreferrer" class="product-link">
                    View Product
                    <svg class="external-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                        <polyline points="15 3 21 3 21 9"></polyline>
                        <line x1="10" x2="21" y1="14" y2="3"></line>
                    </svg>
                </a>
            </div>
        </div>
    `).join('');
}