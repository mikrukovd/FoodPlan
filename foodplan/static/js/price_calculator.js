class PriceCalculator {
    constructor() {
        this.prices = {
            base: 0,
            meals: {
                'завтрак': 100,
                'обед': 300,
                'ужин': 200,
                'десерт': 100
            },
            durations: {
                1: 1.0,    // без скидки
                3: 0.9,    // 10% скидка
                6: 0.8,    // 20% скидка
                12: 0.7    // 30% скидка
            }
        };
        
        this.init();
    }

    init() {
        this.bindEvents();
        this.calculatePrice();
    }

    bindEvents() {
        const formElements = [
            'select[name="duration"]',
            'select[name="has_завтрак"]',
            'select[name="has_обед"]',
            'select[name="has_ужин"]',
            'select[name="has_десерт"]'
        ];

        formElements.forEach(selector => {
            const element = document.querySelector(selector);
            if (element) {
                element.addEventListener('change', () => this.calculatePrice());
            }
        });
    }

    getFormValues() {
        return {
            duration: parseInt(document.querySelector('select[name="duration"]').value) || 1,
            has_завтрак: document.querySelector('select[name="has_завтрак"]').value === 'true',
            has_обед: document.querySelector('select[name="has_обед"]').value === 'true',
            has_ужин: document.querySelector('select[name="has_ужин"]').value === 'true',
            has_десерт: document.querySelector('select[name="has_десерт"]').value === 'true'
        };
    }

    calculatePrice() {
        const values = this.getFormValues();
        let monthlyPrice = this.prices.base;

        // Стоимость относительно приёмов пищи
        if (values.has_завтрак) monthlyPrice += this.prices.meals.завтрак;
        if (values.has_обед) monthlyPrice += this.prices.meals.обед;
        if (values.has_ужин) monthlyPrice += this.prices.meals.ужин;
        if (values.has_десерт) monthlyPrice += this.prices.meals.десерт;

        // Скидка за период
        const durationMultiplier = this.prices.durations[values.duration] || 1.0;
        const totalPrice = monthlyPrice * values.duration * durationMultiplier;

        this.updateDisplay(Math.round(totalPrice));
    }

    updateDisplay(price) {
        const priceElement = document.getElementById('totalPrice');
        if (priceElement) {
            priceElement.textContent = price;
        }
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    new PriceCalculator();
});