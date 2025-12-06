// Sample dataset
const solarProducts = [];

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
    loadCSV(); 
});

function loadCSV() {
    Papa.parse('combined_indiamart_data.csv', {
        download: true,
        header: true,
        skipEmptyLines: true,
        complete: function(results) {
            // assign the CSV rows to your main data variable
            solarProducts = results.data.map(row => ({
                ...row,
                Rating: parseFloat(row.Rating),
                Reviews: parseInt(row.Reviews),
                Price: row.Price
            }));

            // AFTER data is ready → initialize the UI
            initializeCategoryButtons();
            initializeStateSelect();
            initializeEventListeners();
            renderProducts();
        }
    });
}


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