from flask import Flask, render_template_string, request, redirect, jsonify
from datetime import datetime
import json

app = Flask(__name__)

# Data structures
ideas = []
transactions = []
categories = ["Personal", "Business", "Investment", "Savings"]
idea_statuses = ["New", "In Progress", "Completed", "On Hold"]

@app.route("/")
def home():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Osonai - Advanced Banking & Ideas Platform</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <script src="https://unpkg.com/alpinejs" defer></script>
            <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap" rel="stylesheet">
            <style>
                :root {
                    --primary: #6366f1;
                    --secondary: #8b5cf6;
                    --accent: #ec4899;
                    --background: #0f172a;
                    --surface: #1e293b;
                    --text: #f8fafc;
                }
                body {
                    font-family: 'Space Grotesk', sans-serif;
                    background: var(--background);
                    color: var(--text);
                }
                .glass-card {
                    background: rgba(30, 41, 59, 0.7);
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                }
                .gradient-text {
                    background: linear-gradient(135deg, var(--primary), var(--accent));
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                }
                .hover-glow:hover {
                    box-shadow: 0 0 20px rgba(99, 102, 241, 0.3);
                }
                .nav-link {
                    position: relative;
                }
                .nav-link::after {
                    content: '';
                    position: absolute;
                    bottom: -2px;
                    left: 0;
                    width: 0;
                    height: 2px;
                    background: linear-gradient(90deg, var(--primary), var(--accent));
                    transition: width 0.3s ease;
                }
                .nav-link:hover::after {
                    width: 100%;
                }
            </style>
        </head>
        <body class="min-h-screen">
            <div x-data="{ 
                activeTab: 'dashboard',
                newIdea: { title: '', description: '', status: 'New' },
                newTransaction: { amount: '', category: 'Personal', description: '' }
            }" class="container mx-auto px-4 py-8">
                <!-- Navigation -->
                <nav class="glass-card rounded-xl mb-8">
                    <div class="flex justify-between items-center p-6">
                        <h1 class="text-3xl font-bold gradient-text">Osonai</h1>
                        <div class="space-x-6">
                            <button @click="activeTab = 'dashboard'" 
                                class="nav-link px-4 py-2 text-lg" 
                                :class="activeTab === 'dashboard' ? 'text-indigo-400' : 'text-gray-400 hover:text-white'">
                                Dashboard
                            </button>
                            <button @click="activeTab = 'ideas'" 
                                class="nav-link px-4 py-2 text-lg" 
                                :class="activeTab === 'ideas' ? 'text-indigo-400' : 'text-gray-400 hover:text-white'">
                                Ideas
                            </button>
                            <button @click="activeTab = 'banking'" 
                                class="nav-link px-4 py-2 text-lg" 
                                :class="activeTab === 'banking' ? 'text-indigo-400' : 'text-gray-400 hover:text-white'">
                                Banking
                            </button>
                        </div>
                    </div>
                </nav>

                <!-- Dashboard Tab -->
                <div x-show="activeTab === 'dashboard'" class="space-y-8">
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div class="glass-card p-8 rounded-xl hover-glow transition-all duration-300">
                            <h3 class="text-lg font-medium text-gray-400">Total Balance</h3>
                            <p class="text-4xl font-bold gradient-text mt-2">${{ total_balance }}</p>
                        </div>
                        <div class="glass-card p-8 rounded-xl hover-glow transition-all duration-300">
                            <h3 class="text-lg font-medium text-gray-400">Active Ideas</h3>
                            <p class="text-4xl font-bold text-green-400 mt-2">{{ active_ideas_count }}</p>
                        </div>
                        <div class="glass-card p-8 rounded-xl hover-glow transition-all duration-300">
                            <h3 class="text-lg font-medium text-gray-400">Recent Transactions</h3>
                            <p class="text-4xl font-bold text-blue-400 mt-2">{{ recent_transactions_count }}</p>
                        </div>
                    </div>
                    <div class="glass-card p-8 rounded-xl">
                        <canvas id="financialChart"></canvas>
                    </div>
                </div>

                <!-- Ideas Tab -->
                <div x-show="activeTab === 'ideas'" class="space-y-8">
                    <div class="glass-card p-8 rounded-xl">
                        <h2 class="text-2xl font-bold gradient-text mb-6">New Idea</h2>
                        <form @submit.prevent="fetch('/add_idea', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/x-www-form-urlencoded',
                            },
                            body: new URLSearchParams({
                                'title': newIdea.title,
                                'description': newIdea.description,
                                'status': newIdea.status
                            })
                        }).then(response => {
                            if (response.ok) {
                                window.location.reload();
                            }
                        })" class="space-y-6">
                            <div>
                                <label class="block text-sm font-medium text-gray-400">Title</label>
                                <input type="text" x-model="newIdea.title" 
                                    class="mt-2 block w-full rounded-lg bg-slate-800 border-slate-700 text-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-400">Description</label>
                                <textarea x-model="newIdea.description" rows="3" 
                                    class="mt-2 block w-full rounded-lg bg-slate-800 border-slate-700 text-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent"></textarea>
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-400">Status</label>
                                <select x-model="newIdea.status" 
                                    class="mt-2 block w-full rounded-lg bg-slate-800 border-slate-700 text-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
                                    <option value="New">New</option>
                                    <option value="In Progress">In Progress</option>
                                    <option value="Completed">Completed</option>
                                    <option value="On Hold">On Hold</option>
                                </select>
                            </div>
                            <button type="submit" 
                                class="w-full bg-gradient-to-r from-indigo-500 to-purple-500 text-white py-3 px-4 rounded-lg hover:opacity-90 transition-opacity">
                                Add Idea
                            </button>
                        </form>
                    </div>
                    <div class="glass-card p-8 rounded-xl">
                        <h2 class="text-2xl font-bold gradient-text mb-6">Your Ideas</h2>
                        <div class="space-y-4">
                            {% for idea in ideas %}
                            <div class="glass-card p-6 rounded-lg hover-glow transition-all duration-300">
                                <div class="flex justify-between items-start">
                                    <h3 class="font-semibold text-lg">{{ idea.title }}</h3>
                                    <span class="px-3 py-1 text-sm rounded-full" :class="{
                                        'bg-green-900/50 text-green-400': idea.status === 'Completed',
                                        'bg-yellow-900/50 text-yellow-400': idea.status === 'In Progress',
                                        'bg-blue-900/50 text-blue-400': idea.status === 'New',
                                        'bg-gray-900/50 text-gray-400': idea.status === 'On Hold'
                                    }">{{ idea.status }}</span>
                                </div>
                                <p class="text-gray-400 mt-3">{{ idea.description }}</p>
                                <div class="mt-4 flex space-x-4">
                                    <button class="text-indigo-400 hover:text-indigo-300 transition-colors">Edit</button>
                                    <button @click="fetch('/delete_idea', {
                                        method: 'POST',
                                        headers: {
                                            'Content-Type': 'application/x-www-form-urlencoded',
                                        },
                                        body: new URLSearchParams({
                                            'index': '{{ loop.index0 }}'
                                        })
                                    }).then(response => {
                                        if (response.ok) {
                                            window.location.reload();
                                        }
                                    })" class="text-red-400 hover:text-red-300 transition-colors">Delete</button>
                                </div>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                </div>

                <!-- Banking Tab -->
                <div x-show="activeTab === 'banking'" class="space-y-8">
                    <div class="glass-card p-8 rounded-xl">
                        <h2 class="text-2xl font-bold gradient-text mb-6">New Transaction</h2>
                        <form @submit.prevent="fetch('/add_transaction', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/x-www-form-urlencoded',
                            },
                            body: new URLSearchParams({
                                'amount': newTransaction.amount,
                                'category': newTransaction.category,
                                'description': newTransaction.description
                            })
                        }).then(response => {
                            if (response.ok) {
                                window.location.reload();
                            }
                        })" class="space-y-6">
                            <div>
                                <label class="block text-sm font-medium text-gray-400">Amount</label>
                                <input type="number" x-model="newTransaction.amount" 
                                    class="mt-2 block w-full rounded-lg bg-slate-800 border-slate-700 text-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-400">Category</label>
                                <select x-model="newTransaction.category" 
                                    class="mt-2 block w-full rounded-lg bg-slate-800 border-slate-700 text-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
                                    {% for category in categories %}
                                    <option value="{{ category }}">{{ category }}</option>
                                    {% endfor %}
                                </select>
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-400">Description</label>
                                <input type="text" x-model="newTransaction.description" 
                                    class="mt-2 block w-full rounded-lg bg-slate-800 border-slate-700 text-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
                            </div>
                            <button type="submit" 
                                class="w-full bg-gradient-to-r from-indigo-500 to-purple-500 text-white py-3 px-4 rounded-lg hover:opacity-90 transition-opacity">
                                Add Transaction
                            </button>
                        </form>
                    </div>
                    <div class="glass-card p-8 rounded-xl">
                        <h2 class="text-2xl font-bold gradient-text mb-6">Transaction History</h2>
                        <div class="overflow-x-auto">
                            <table class="min-w-full">
                                <thead>
                                    <tr class="border-b border-slate-700">
                                        <th class="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Date</th>
                                        <th class="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Amount</th>
                                        <th class="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Category</th>
                                        <th class="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Description</th>
                                        <th class="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Actions</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-slate-700">
                                    {% for transaction in transactions %}
                                    <tr class="hover:bg-slate-800/50 transition-colors">
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-400">{{ transaction.date }}</td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm" :class="transaction.amount >= 0 ? 'text-green-400' : 'text-red-400'">
                                            ${{ transaction.amount }}
                                        </td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-400">{{ transaction.category }}</td>
                                        <td class="px-6 py-4 text-sm text-gray-400">{{ transaction.description }}</td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm">
                                            <button @click="fetch('/delete_transaction', {
                                                method: 'POST',
                                                headers: {
                                                    'Content-Type': 'application/x-www-form-urlencoded',
                                                },
                                                body: new URLSearchParams({
                                                    'index': '{{ loop.index0 }}'
                                                })
                                            }).then(response => {
                                                if (response.ok) {
                                                    window.location.reload();
                                                }
                                            })" class="text-red-400 hover:text-red-300 transition-colors">Delete</button>
                                        </td>
                                    </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>

            <script>
                // Initialize Chart.js with custom styling
                const ctx = document.getElementById('financialChart').getContext('2d');
                new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                        datasets: [{
                            label: 'Balance',
                            data: [1200, 1900, 3000, 5000, 2000, 3000],
                            borderColor: '#6366f1',
                            backgroundColor: 'rgba(99, 102, 241, 0.1)',
                            borderWidth: 2,
                            tension: 0.4,
                            pointBackgroundColor: '#6366f1',
                            pointBorderColor: '#fff',
                            pointRadius: 4,
                            pointHoverRadius: 6
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                labels: {
                                    color: '#f8fafc',
                                    font: {
                                        family: "'Space Grotesk', sans-serif"
                                    }
                                }
                            },
                            title: {
                                display: true,
                                text: 'Financial Overview',
                                color: '#f8fafc',
                                font: {
                                    family: "'Space Grotesk', sans-serif",
                                    size: 16
                                }
                            }
                        },
                        scales: {
                            y: {
                                grid: {
                                    color: 'rgba(255, 255, 255, 0.1)'
                                },
                                ticks: {
                                    color: '#f8fafc'
                                }
                            },
                            x: {
                                grid: {
                                    color: 'rgba(255, 255, 255, 0.1)'
                                },
                                ticks: {
                                    color: '#f8fafc'
                                }
                            }
                        }
                    }
                });
            </script>
        </body>
        </html>
    ''', ideas=ideas, categories=categories, idea_statuses=idea_statuses,
    total_balance=sum(t.get('amount', 0) for t in transactions),
    active_ideas_count=len([i for i in ideas if i.get('status') != 'Completed']),
    recent_transactions_count=len(transactions))

@app.route("/add_idea", methods=["POST"])
def add_idea():
    idea = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'status': request.form.get('status', 'New'),
        'created_at': datetime.now().isoformat()
    }
    ideas.append(idea)
    return redirect("/")

@app.route("/add_transaction", methods=["POST"])
def add_transaction():
    transaction = {
        'amount': float(request.form.get('amount', 0)),
        'category': request.form.get('category'),
        'description': request.form.get('description'),
        'date': datetime.now().strftime('%Y-%m-%d %H:%M')
    }
    transactions.append(transaction)
    return redirect("/")

@app.route("/delete_idea", methods=["POST"])
def delete_idea():
    index = int(request.form.get('index'))
    if 0 <= index < len(ideas):
        ideas.pop(index)
    return redirect("/")

@app.route("/delete_transaction", methods=["POST"])
def delete_transaction():
    index = int(request.form.get('index'))
    if 0 <= index < len(transactions):
        transactions.pop(index)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=False)
