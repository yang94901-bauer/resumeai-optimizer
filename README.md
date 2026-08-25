# ResumeAI - AI English Resume Optimizer

AI-powered tool that translates Chinese resumes to professional, ATS-optimized English resumes.

## Tech Stack
- **Backend**: Python Flask
- **AI**: Kimi (Moonshot) API
- **Payment**: Lemon Squeezy
- **Frontend**: Vanilla HTML/CSS/JS

## Local Development

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set environment variables
```bash
export KIMI_API_KEY="your-kimi-api-key"
export LEMON_SQUEEZY_API_KEY="your-ls-api-key"
export LEMON_SQUEEZY_PRODUCT_ID="your-product-id"
```

### 3. Run
```bash
python app.py
```

Open http://localhost:5000

## Deployment (Railway / Render / Heroku)

### Environment Variables Required:
- `KIMI_API_KEY` - Your Moonshot/Kimi API key
- `LEMON_SQUEEZY_API_KEY` - Lemon Squeezy API key
- `LEMON_SQUEEZY_PRODUCT_ID` - Product ID for checkout
- `PORT` - Auto-set by most platforms

### Deploy to Railway:
1. Push this repo to GitHub
2. Connect repo in Railway
3. Add environment variables
4. Deploy

## API Endpoints

### POST /api/optimize
Optimize a Chinese resume to English.
```json
{
  "resume": "中文简历内容..."
}
```

### POST /api/cover-letter
Generate a cover letter.
```json
{
  "resume": "简历内容",
  "job_description": "职位描述（可选）"
}
```

### POST /api/verify-payment
Verify Lemon Squeezy payment.
```json
{
  "order_id": "订单ID"
}
```

## Pricing
- Resume Optimization: $9.90
- Cover Letter: $4.90

## Lemon Squeezy Setup
1. Create a product in Lemon Squeezy dashboard
2. Set up webhook to `/api/verify-payment`
3. Add checkout button in frontend (replace `proceedToPayment()` function)
