# Vault AI Platform - Web Interface User Manual

**Version**: 2.0.0
**Date**: 2025-11-19
**For**: Non-Technical Users
**Interface**: Web-Based Graphical Interface

---

## 📋 Table of Contents

1. [Getting Started](#getting-started)
2. [Dashboard Overview](#dashboard-overview)
3. [AI Agents Guide](#ai-agents-guide)
   - [Legal Research Agent](#1-legal-research-agent)
   - [HR Policy Agent](#2-hr-policy-agent)
   - [Customer Service Agent](#3-customer-service-agent)
   - [Analysis Agent](#4-analysis-agent)
   - [Synthesis Agent](#5-synthesis-agent)
   - [Validation Agent](#6-validation-agent)
4. [Other Features](#other-features)
5. [Tips & Best Practices](#tips--best-practices)
6. [Troubleshooting](#troubleshooting)
7. [FAQs](#faqs)

---

## Getting Started

### Accessing the Platform

1. **Open your web browser** (Chrome, Firefox, Safari, or Edge)
2. **Navigate to**: `http://localhost:8000`
3. **You'll see** the Vault AI Platform dashboard

**No login required!** The platform is ready to use immediately.

---

### First Time User Checklist

✅ **Check System Status**
- Look at the top of the page
- You should see: "System Healthy" with a green dot
- If it says "System Unhealthy", wait 30 seconds and refresh the page

✅ **Familiarize with Navigation**
- See 5 main tabs at the top
- Default view is "🤖 AI Agents"

✅ **Try a Simple Test**
- Click "⚖️ Legal Research" (first agent)
- Type: "What is the Companies Ordinance about?"
- Click "🔍 Research Legal Question"
- Wait for results (first query may take 1-2 minutes)

---

## Dashboard Overview

### Header Section

```
┌─────────────────────────────────────────────────┐
│ 🤖 Vault AI Platform                            │
│ Multi-Domain Agentic AI Platform                │
│ ● System Healthy                                │
└─────────────────────────────────────────────────┘
```

**What you see:**
- **Platform Name**: Vault AI Platform
- **Status Indicator**: Green dot = Healthy, Red dot = Issue
- **Status Text**: "System Healthy" or "System Unhealthy"

---

### Main Navigation Tabs

You'll see 5 main tabs:

| Tab | Icon | Purpose | When to Use |
|-----|------|---------|-------------|
| **AI Agents** | 🤖 | Interactive AI assistants | Most common - daily tasks |
| **Workflows** | 🔄 | Multi-agent processes | Complex tasks |
| **Text Generation** | 💬 | Direct AI writing | Creative writing, general questions |
| **Models** | 🤖 | View AI models | Check what's installed |
| **API Docs** | 📚 | Technical documentation | Developers only |

**Default Tab**: AI Agents (opens automatically)

---

## AI Agents Guide

The **AI Agents** tab is your main workspace. You'll see **6 specialized agents**, each designed for specific tasks.

### Agent Selection

When you open the platform, you'll see:

```
┌─────────────────────────────────────────────────┐
│ 🤖 AI Agents - Specialized Domain Experts       │
│                                                  │
│ [⚖️ Legal Research] [👥 HR Policy] [💬 CS]...  │
│                                                  │
│ [Agent workspace appears here]                  │
└─────────────────────────────────────────────────┘
```

**Click any agent button** to switch between agents.

---

## 1. ⚖️ Legal Research Agent

### What It Does
Searches **1,699 Hong Kong ordinances** and answers your legal questions with sources from actual laws.

### When to Use
- Understanding HK laws and regulations
- Company compliance questions
- Director responsibilities
- Building management requirements
- Employment law queries
- Any question about Hong Kong ordinances

### How to Use

#### Step 1: Click "⚖️ Legal Research"
The agent button is the first one in the sub-tabs.

#### Step 2: Enter Your Question
In the text box, type your legal question in plain English.

**Good Examples:**
- "What are director duties under the Companies Ordinance?"
- "What are insurance requirements for building management?"
- "What are the legal requirements for employment contracts?"
- "How should annual general meetings be conducted?"

**Not-So-Good Examples:**
- "Tell me about law" (too vague)
- "CAP 32" (use natural language instead)

#### Step 3: Click "🔍 Research Legal Question"
The blue button at the bottom.

#### Step 4: Wait for Results
- **First time**: May take 60-120 seconds (AI is loading)
- **Subsequent queries**: 10-30 seconds
- You'll see a loading animation with a message

#### Step 5: Review Results
You'll see:
1. **Answer**: AI-generated response based on HK laws
2. **Agent Info**: Which agent processed your request
3. **Time**: How long it took
4. **Sources**: Legal references from actual ordinances (if applicable)

### Example Session

**Question**: "What are the director duties under the Companies Ordinance?"

**Result**:
```
⚖️ Legal Research Result

Answer:
Under the Hong Kong Companies Ordinance, directors have several
key fiduciary duties including:

1. Duty to act in good faith in the interests of the company
2. Duty to exercise powers for proper purposes
3. Duty to avoid conflicts of interest
4. Duty of care, skill and diligence
...

📚 Sources
1. Companies Ordinance (Cap. 622) - Section 465
   "A director of a company must act honestly and in good faith..."

2. Companies Ordinance (Cap. 622) - Section 466
   "A director must exercise the care, skill and diligence..."
```

### Tips
✅ **Ask specific questions** for better answers
✅ **Use full sentences** instead of keywords
✅ **Mention ordinance names** if you know them
✅ **First query is slow** - this is normal
✅ **Check sources** to verify the legal basis

---

## 2. 👥 HR Policy Agent

### What It Does
Answers questions about HR policies, benefits, vacation, and employee procedures based on your company documents.

### When to Use
- Employee handbook questions
- Vacation day calculations
- Benefits inquiries
- Leave policies
- HR procedure clarifications
- Onboarding questions

### How to Use

#### Step 1: Click "👥 HR Policy"
Second agent button in the sub-tabs.

#### Step 2: Enter Your Question
Type your HR-related question.

**Examples:**
- "How many vacation days after 3 years?"
- "What is the parental leave policy?"
- "Am I eligible for health insurance?"
- "How do I request time off?"

#### Step 3: (Optional) Paste Your Policy Documents
If you have HR policy documents, paste them in the **"Policy Context"** box.

**Why?** The AI will analyze YOUR specific policies instead of giving general answers.

**What to paste:**
- Employee handbook sections
- Vacation policies
- Benefits documentation
- Leave policies
- Any relevant HR documents

#### Step 4: Click "💼 Get HR Answer"

#### Step 5: Review Results
You'll get an answer based on:
- Your specific policies (if provided)
- General HR best practices (if no context given)

### Example Session

**Question**: "How many vacation days do employees get after 3 years?"

**Policy Context**:
```
VACATION POLICY
New employees: 10 days per year
After 1 year: 15 days per year
After 3 years: 20 days per year
After 5 years: 25 days per year

Vacation requests require 2 weeks advance notice and
manager approval.
```

**Result**:
```
👥 HR Policy Answer

Based on the policy you provided, employees with 3 years
of service receive 20 days of vacation per year.

Note: Vacation requests must be submitted at least 2 weeks
in advance and require manager approval.
```

### Tips
✅ **Paste relevant policies** for accurate answers
✅ **Be specific** about tenure/status (full-time, part-time)
✅ **Copy from official documents** for best results
✅ **Use this for quick lookups** instead of reading entire handbooks

---

## 3. 💬 Customer Service Agent

### What It Does
Provides support answers based on your product documentation, FAQs, and help guides.

### When to Use
- Customer support inquiries
- Product questions
- Troubleshooting help
- How-to guides
- Account management
- Password resets

### How to Use

#### Step 1: Click "💬 Customer Service"
Third agent button in the sub-tabs.

#### Step 2: Enter Support Question

**Examples:**
- "How do I reset my password?"
- "How do I create a new account?"
- "What payment methods are accepted?"
- "How do I cancel my subscription?"

#### Step 3: (Optional) Paste Documentation
Add relevant support docs, FAQs, or guides in **"Support Documentation"**.

**What to paste:**
- FAQ sections
- User guides
- Troubleshooting docs
- Account management procedures
- Product manuals

#### Step 4: Click "🎫 Get Support Answer"

#### Step 5: Review Step-by-Step Instructions

### Example Session

**Question**: "How do I reset my password?"

**Documentation**:
```
PASSWORD RESET PROCEDURE
1. Go to the login page
2. Click "Forgot Password" link
3. Enter your registered email address
4. Check your email for a reset link (valid 24 hours)
5. Click the link and create a new password
6. Password requirements: 8+ characters, uppercase,
   lowercase, and numbers

If you don't receive the email within 5 minutes,
check your spam folder or contact support@example.com
```

**Result**:
```
💬 Support Answer

To reset your password, follow these steps:

1. Navigate to the login page
2. Click the "Forgot Password" link
3. Enter your registered email address
4. Check your inbox for a password reset link
   (the link expires in 24 hours)
5. Click the link and create your new password
   • Must be at least 8 characters
   • Must include uppercase and lowercase letters
   • Must include numbers

Troubleshooting:
If you don't receive the email within 5 minutes,
check your spam folder. If still not received,
contact support@example.com for assistance.
```

### Tips
✅ **Paste your actual docs** for accurate answers
✅ **Ask one question at a time** for clarity
✅ **Include error messages** if troubleshooting
✅ **Use for self-service support** - faster than email

---

## 4. 📊 Analysis Agent

### What It Does
Extracts insights, trends, and key findings from text data like reports, surveys, or feedback.

### When to Use
- Analyzing sales reports
- Understanding survey results
- Extracting KPIs from data
- Identifying trends
- Summarizing large documents
- Finding action items

### How to Use

#### Step 1: Click "📊 Analysis"
Fourth agent button in the sub-tabs.

#### Step 2: Paste Your Text
In the large text box, paste the content you want analyzed.

**What you can analyze:**
- Quarterly reports
- Customer feedback
- Survey results
- Meeting notes
- Market research
- Performance data

#### Step 3: (Optional) Specify Focus
In "Analysis Focus", tell the AI what to focus on.

**Examples:**
- "Identify key performance indicators"
- "Find trends and patterns"
- "Extract action items"
- "Highlight risks and opportunities"
- "Summarize main findings"

#### Step 4: Click "📈 Analyze"

#### Step 5: Review Insights

### Example Session

**Text to Analyze**:
```
Q4 2024 Performance Summary

Revenue increased 25% to $5.2M compared to Q3.
New product line contributed $2.1M (40% of total revenue).
We expanded to APAC, EU, and LATAM markets.

Customer retention improved from 65% to 78%.
Customer acquisition cost decreased 20% through
optimized digital marketing.

Operating costs increased 15% due to new hires
and infrastructure investments.
Net profit margin stands at 18%.
```

**Focus**: "Identify key performance indicators and trends"

**Result**:
```
📊 Analysis Results

Key Performance Indicators:

1. Revenue Growth: +25% QoQ ($5.2M)
   • Strong positive trend
   • New product line highly successful (40% contribution)

2. Customer Retention: 78% (up from 65%)
   • Significant improvement (+13 percentage points)
   • Indicates better customer satisfaction

3. Customer Acquisition Cost: -20%
   • Marketing optimization working well
   • Better ROI on acquisition spend

4. Geographic Expansion: 3 new markets (APAC, EU, LATAM)
   • Diversification strategy in progress

5. Net Profit Margin: 18%
   • Healthy despite 15% increase in operating costs

Trends:
✓ Growth trajectory is strong
✓ Efficient customer acquisition
✓ Successful product innovation
⚠ Operating costs rising (monitor closely)

Recommendations:
1. Continue new product development
2. Maintain customer retention initiatives
3. Monitor operating cost efficiency
4. Track new market performance
```

### Tips
✅ **Paste complete documents** for comprehensive analysis
✅ **Be specific in focus** to get targeted insights
✅ **Use for long reports** - saves reading time
✅ **Try different focus areas** for various perspectives

---

## 5. 🔗 Synthesis Agent

### What It Does
Combines information from multiple sources into a comprehensive, unified analysis.

### When to Use
- Comparing different reports
- Combining survey results
- Creating summaries from multiple sources
- Finding common themes
- Building comprehensive plans
- Cross-referencing information

### How to Use

#### Step 1: Click "🔗 Synthesis"
Fifth agent button in the sub-tabs.

#### Step 2: Fill in Source Documents
You'll see 3 source containers by default:
- **Title**: Name of the source (e.g., "Customer Survey")
- **Content**: Paste the actual content

**Minimum**: 2 sources required
**Maximum**: Add as many as needed with "+ Add Another Source" button

#### Step 3: Add More Sources (Optional)
Click **"+ Add Another Source"** to add more.

#### Step 4: Specify Synthesis Focus (Optional)
Tell the AI what to focus on when combining sources.

**Examples:**
- "Create comprehensive improvement plan"
- "Identify common themes"
- "Compare and contrast findings"
- "Build action plan"

#### Step 5: Click "🔗 Synthesize"

#### Step 6: Review Combined Analysis

### Example Session

**Source 1 - Customer Survey**:
```
Title: Q4 Customer Satisfaction Survey
Content: 85% satisfaction rate. Top request: mobile app
development. Pricing rated as excellent (4.5/5).
Customer support rated 4.5/5 stars. Response time needs
improvement (3.2/5).
```

**Source 2 - App Store Reviews**:
```
Title: App Store Feedback Analysis
Content: 4.2 star average rating. Users praise ease of use
and clean interface. Main complaints: occasional crashes on
iOS 16, slow sync times. Top feature requests: dark mode
(mentioned 47 times), offline access (mentioned 38 times).
```

**Source 3 - Support Tickets**:
```
Title: November Support Ticket Summary
Content: 240 tickets total. Main issues: sync delays (35%),
password reset problems (25%), billing questions (20%),
feature requests (20%). Average resolution time: 4.5 hours.
```

**Focus**: "Create comprehensive product improvement plan"

**Result**:
```
🔗 Synthesis Results

COMPREHENSIVE PRODUCT IMPROVEMENT PLAN

1. CRITICAL PRIORITIES (High Impact, High Urgency)

a) Sync Performance Issues
   • Source: Support tickets (35%), App reviews
   • Impact: User experience, retention
   • Action: Optimize sync engine, reduce latency

b) iOS 16 Crash Bug
   • Source: App store reviews
   • Impact: User satisfaction, ratings
   • Action: Debug and patch immediately

2. HIGH PRIORITY FEATURES (High Demand)

a) Mobile App Development
   • Source: Customer survey (top request)
   • Demand: Very high
   • Action: Begin development sprint

b) Dark Mode
   • Source: App reviews (47 mentions)
   • Demand: High
   • Action: UI/UX design, implementation

c) Offline Access
   • Source: App reviews (38 mentions)
   • Demand: High
   • Action: Plan data caching strategy

3. OPERATIONAL IMPROVEMENTS

a) Support Response Time
   • Source: Survey (3.2/5 rating)
   • Current: 4.5 hours average
   • Action: Reduce to <2 hours, add chat support

b) Password Reset Flow
   • Source: Support tickets (25%)
   • Impact: User frustration
   • Action: Simplify process, add self-service

4. STRENGTHS TO MAINTAIN

✓ Pricing strategy (4.5/5)
✓ Customer support quality (4.5/5)
✓ Interface usability
✓ Overall satisfaction (85%)

RECOMMENDED TIMELINE:
Week 1-2: Fix iOS crash, improve sync
Week 3-6: Develop mobile app MVP
Week 7-8: Implement dark mode
Month 2-3: Add offline access
Ongoing: Improve support response times
```

### Tips
✅ **Use diverse sources** for comprehensive insights
✅ **At least 2 sources required** to synthesize
✅ **Add clear titles** to organize sources
✅ **Good for research projects** requiring multiple inputs
✅ **Specify focus** for targeted synthesis

---

## 6. ✅ Validation Agent

### What It Does
Checks consistency across multiple documents and identifies discrepancies or conflicts.

### When to Use
- Verifying policy consistency
- Cross-checking data accuracy
- Finding document conflicts
- Quality control
- Compliance checking
- Error detection

### How to Use

#### Step 1: Click "✅ Validation"
Sixth agent button in the sub-tabs.

#### Step 2: Fill in Documents to Validate
Similar to Synthesis, you'll see 3 document containers:
- **Title**: Document name
- **Content**: Paste the document content

**Minimum**: 2 documents required
**Maximum**: Add more with "+ Add Another Document" button

#### Step 3: Specify Validation Focus (Optional)
Tell the AI what to check for.

**Examples:**
- "Check for inconsistencies in vacation policy"
- "Verify pricing accuracy"
- "Find conflicting information"
- "Check policy consistency"

#### Step 4: Click "✓ Validate"

#### Step 5: Review Inconsistencies Report

### Example Session

**Document 1 - Employee Handbook**:
```
Title: Employee Handbook 2024
Content: VACATION POLICY: Full-time employees receive
15 days paid vacation per year. Part-time employees
receive 7 days per year. Vacation accrual begins on
the hire date.
```

**Document 2 - HR Website**:
```
Title: Company HR Portal
Content: All employees receive 15 days of paid vacation
annually. Vacation time accrues starting from your
first day of employment.
```

**Document 3 - Offer Letter Template**:
```
Title: Standard Offer Letter
Content: You will receive 10 days of paid vacation
during your first year of employment. After completing
one year of service, your vacation allowance increases
to 15 days per year.
```

**Focus**: "Check for inconsistencies in vacation policy"

**Result**:
```
✅ Validation Results

INCONSISTENCIES DETECTED

⚠️ CRITICAL INCONSISTENCY #1: First Year Vacation Days

Document 1 (Employee Handbook):
• States: "Full-time employees receive 15 days"
• Interpretation: 15 days from start

Document 2 (HR Website):
• States: "All employees receive 15 days"
• Interpretation: 15 days from start

Document 3 (Offer Letter):
• States: "10 days during your first year"
• Interpretation: Only 10 days year one

CONFLICT: Documents 1 & 2 say 15 days immediately,
Document 3 says 10 days first year.

⚠️ INCONSISTENCY #2: Part-Time Employees

Document 1 (Employee Handbook):
• States: "Part-time employees receive 7 days"

Document 2 (HR Website):
• States: "All employees receive 15 days"

CONFLICT: Website doesn't differentiate between
full-time and part-time employees.

✓ CONSISTENCY #1: Accrual Start Date

All documents agree: Vacation accrues from hire date.

RECOMMENDATIONS:

1. URGENT: Clarify first-year vacation policy
   • Update Offer Letter to match Handbook OR
   • Update Handbook to reflect graduated schedule

2. Update HR Website
   • Add part-time employee vacation details
   • Clarify 7-day policy for part-time staff

3. Create Single Source of Truth
   • Designate Employee Handbook as authoritative
   • Update all other documents to match

4. Version Control
   • Add "Last Updated" dates to all policies
   • Implement quarterly policy review process
```

### Tips
✅ **Use official documents** for validation
✅ **Check before publishing** policies
✅ **Good for compliance** audits
✅ **Catches errors** humans might miss
✅ **At least 2 documents** required

---

## Other Features

### 🔄 Workflows Tab

**What it is**: Pre-built processes that use multiple agents together.

**Available Workflows:**
- HR Onboarding
- CS Ticket Response
- Legal-HR Compliance
- Simple Q&A
- Multi-Agent Research

**How to use**:
1. Click "🔄 Workflows" tab
2. View available workflows
3. Click "View Workflow API Documentation" for details

**Note**: Workflows are currently API-based. Contact your administrator for integration.

---

### 💬 Text Generation Tab

**What it is**: Direct AI writing without specialized agent logic.

**When to use**:
- Creative writing
- General questions
- Custom prompts
- Testing AI capabilities

**How to use**:
1. Click "💬 Text Generation" tab
2. (Optional) Enter a system prompt (e.g., "You are a helpful assistant")
3. Enter your main prompt
4. Adjust Max Tokens (length) and Temperature (creativity)
5. Click "Generate Response"

**Settings**:
- **Max Tokens**: How long the response should be (50-4096)
- **Temperature**: How creative (0 = focused, 1 = creative)

---

### 🤖 Models Tab

**What it is**: View installed AI models.

**How to use**:
1. Click "🤖 Models" tab
2. Click "🔄 Refresh Models"
3. See all installed models with details

**You'll see**:
- Model names
- File sizes
- Active models (badges)
- Parameters and quantization
- Last modified dates

**Note**: For viewing only. Model management requires administrator access.

---

### 📚 API Docs Tab

**What it is**: Technical documentation and dashboards.

**Links provided**:
- Interactive API Docs (Swagger)
- ReDoc Documentation
- Qdrant Vector DB Dashboard

**Who needs this**: Developers and administrators only.

---

## Tips & Best Practices

### Getting Better Results

#### ✅ **Be Specific**
❌ Bad: "Tell me about law"
✅ Good: "What are director duties under the Companies Ordinance?"

#### ✅ **Provide Context**
Use the context boxes (HR Policy, Customer Service) for more accurate answers.

#### ✅ **Use Full Sentences**
❌ Bad: "vacation days"
✅ Good: "How many vacation days do employees with 3 years get?"

#### ✅ **One Question at a Time**
Break complex queries into separate questions for clarity.

---

### Performance Tips

#### ⏱️ **First Query is Slow**
The first time you use any agent, it may take 60-120 seconds. This is the AI "warming up." Subsequent queries are much faster (10-30 seconds).

#### 🔄 **Keep the Browser Open**
Don't close the browser tab between queries to maintain performance.

#### 📊 **Check Status Indicator**
Green dot = Ready to use
Red dot = System issue (wait 30 seconds and refresh)

---

### Saving Your Work

#### 📋 **Copy Results**
- Select and copy the results you need
- Paste into your documents
- **Note**: Platform doesn't save history automatically

#### 💾 **Save Important Queries**
Keep a document with your common questions for quick reference.

---

## Troubleshooting

### Problem: Page Won't Load

**Solution**:
1. Check you're using: `http://localhost:8000`
2. Refresh the page (F5 or Ctrl+R)
3. Clear browser cache
4. Try a different browser

---

### Problem: "System Unhealthy" Status

**Solution**:
1. Wait 30 seconds
2. Refresh the page
3. If still unhealthy after 2 minutes, contact administrator

---

### Problem: Query Takes Forever (>5 minutes)

**Solution**:
1. **First query**: Wait up to 2 minutes - this is normal
2. **Subsequent queries**: Refresh page and try again
3. Try a simpler question first
4. Check "System Healthy" status

---

### Problem: "Failed to Execute Agent" Error

**Solution**:
1. Check internet connection
2. Refresh the page
3. Verify "System Healthy" status
4. Try again with a different question
5. Contact administrator if persists

---

### Problem: No Results Returned

**Solution**:
1. **Legal Agent**: Check if question is about HK law
2. **Other Agents**: Make sure you pasted context documents
3. Try rephrasing your question
4. Simplify your query

---

### Problem: Agent Returns Generic Answer

**Solution**:
1. Paste your specific documents in context boxes
2. Be more specific in your question
3. Add more details about what you need

---

## FAQs

### General Questions

**Q: Do I need to create an account?**
A: No! The platform is ready to use immediately.

**Q: Is my data saved?**
A: No. Each query is processed independently. Copy important results.

**Q: Can I use this on my phone?**
A: Yes! The interface is mobile-responsive.

**Q: How many queries can I make?**
A: Unlimited! Use as much as you need.

**Q: Which browser should I use?**
A: Chrome, Firefox, Safari, or Edge all work fine.

---

### Legal Research Questions

**Q: How many ordinances are included?**
A: 1,699 Hong Kong ordinances are searchable.

**Q: Is the legal information up to date?**
A: Check with your administrator for the data version date.

**Q: Can I get legal advice?**
A: No. This is for research only. Consult a lawyer for legal advice.

**Q: Why does the first query take so long?**
A: The AI needs to load into memory. This only happens once per session.

---

### HR & Customer Service Questions

**Q: Why should I paste documents?**
A: The AI can't read your company's internal policies. Pasting them ensures accurate, company-specific answers.

**Q: What if I don't have the document?**
A: The AI will provide general best-practice answers, but they may not match your specific policies.

**Q: Can I paste confidential information?**
A: Check with your administrator about data privacy policies.

---

### Technical Questions

**Q: What AI model is used?**
A: Currently llama3.1:8b. Check the "Models" tab for details.

**Q: How accurate are the results?**
A: Very accurate for legal research (based on actual ordinances). For other agents, accuracy depends on the context you provide.

**Q: Can I integrate this with other tools?**
A: Yes, via API. Contact your administrator.

**Q: Why are some agents slower than others?**
A: Legal and Analysis agents process more data. All agents improve after the first query.

---

## Getting Help

### Support Resources

1. **This Manual**: Reference this document first
2. **API Docs Tab**: Technical documentation (for developers)
3. **Your Administrator**: For access issues or bugs
4. **Try Different Phrasings**: Sometimes rephrasing helps

---

### Quick Reference

**Platform URL**: `http://localhost:8000`

**6 AI Agents**:
- ⚖️ Legal Research (HK ordinances)
- 👥 HR Policy (company policies)
- 💬 Customer Service (support docs)
- 📊 Analysis (extract insights)
- 🔗 Synthesis (combine sources)
- ✅ Validation (check consistency)

**Response Times**:
- First query: 60-120 seconds
- Subsequent: 10-30 seconds

**Status Check**: Green dot at top = Ready to use

---

## Appendix: Example Use Cases

### Use Case 1: New Employee Onboarding

**Scenario**: New hire needs to understand benefits

**Steps**:
1. Open platform → Click "👥 HR Policy"
2. Paste employee handbook in context box
3. Ask: "What health insurance benefits am I eligible for?"
4. Get instant answer
5. Ask follow-up: "When does coverage start?"

**Time Saved**: 30 minutes of reading handbook

---

### Use Case 2: Legal Compliance Check

**Scenario**: Understand director responsibilities

**Steps**:
1. Open platform → "⚖️ Legal Research" is default
2. Ask: "What are the statutory duties of directors in Hong Kong?"
3. Review answer with legal sources
4. Ask follow-up: "What are penalties for breach of duties?"

**Time Saved**: Hours of legal research

---

### Use Case 3: Product Feedback Analysis

**Scenario**: Understand customer sentiment from multiple sources

**Steps**:
1. Click "🔗 Synthesis" agent
2. Paste Survey data in Source 1
3. Paste App reviews in Source 2
4. Paste Support tickets in Source 3
5. Focus: "Create improvement plan"
6. Get comprehensive analysis

**Time Saved**: Days of manual analysis

---

### Use Case 4: Policy Consistency Audit

**Scenario**: Ensure vacation policy is consistent across documents

**Steps**:
1. Click "✅ Validation" agent
2. Paste Handbook in Doc 1
3. Paste Website in Doc 2
4. Paste Offer Letter in Doc 3
5. Focus: "Check vacation policy consistency"
6. Get inconsistency report

**Time Saved**: Hours of manual comparison

---

## Conclusion

The Vault AI Platform provides powerful AI assistance through an easy-to-use web interface. **No coding required** - just click, type, and get intelligent answers.

**Remember**:
- 🎯 **Start with AI Agents** - most common use case
- 📋 **Paste context** for better answers
- ⏱️ **First query is slow** - be patient
- 💾 **Copy results** - not saved automatically
- ✅ **Check green dot** - system healthy

**Ready to start?** Open `http://localhost:8000` and begin exploring!

---

**End of User Manual**
Version 2.0.0 | Updated: 2025-11-19
For questions or support, contact your platform administrator.
