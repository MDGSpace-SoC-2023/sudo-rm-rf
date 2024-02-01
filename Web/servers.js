const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const bcrypt = require('bcryptjs');
const User = require('./models/User');
const path = require('path');

const app = express();

app.use(express.static(path.join(__dirname, 'public')));

// Body parser middleware
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// MongoDB Configuration
const db = require('./config/keys').mongoURI;

// Connect to MongoDB
mongoose
  .connect(db, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('MongoDB Connected'))
  .catch(err => console.log(err));
  
// Routes
const users = require('./routes/user');
app.use('/api/users', users);

app.use(bodyParser.urlencoded({ extended: false}));

// Login route handler
app.post('api/users/login', async (req, res) => {
    const { username, password } = req.body;

    try {
        // Find user by username and password
        const user = await User.findOne({ username, password });

        if (user) {
            // Redirect to home page or send a success response
            res.redirect('/home.html');
        } else {
            res.send('Invalid credentials'); // Display error message
        }
    } catch (error) {
        console.error('Login error:', error);
        res.status(500).send('Internal Server Error'); // Handle server error
    }
});

// Define routes for other pages, such as the home page
app.get('/home', (req, res) => {
    res.send('Hello, welcome to the home page');
});

const port = process.env.PORT || 5000;

app.listen(port, () => console.log(`Server running on port ${port}`));
