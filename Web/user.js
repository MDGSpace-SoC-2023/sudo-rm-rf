const express = require('express');
const app = require('../server.js')
const bodyParser = require('body-parser');
const router = express.Router();
const bcrypt = require('bcryptjs');
const User = require('../models/User');
const path = require('path');

// app.use(bodyParser.urlencoded({ extended: false }));
console.log(app)
app.get('/myname', (req, res) =>{
  console.log('Hello')
  res.send('hello there')
  res.end()
});


// Register Route
router.post('/register', (req, res) => {
  const { username, email, password } = req.body;

  // Check if user already exists
  User.findOne({ email }).then(user => {
    if (user) {
      return res.status(400).json({ email: 'Email already exists' });
    } else {
      const newUser = new User({
        username,
        email,
        password
      });

      // Hash password before saving in database
      bcrypt.genSalt(10, (err, salt) => {
        bcrypt.hash(newUser.password, salt, (err, hash) => {
          if (err) throw err;
          newUser.password = hash;
          newUser
            .save()
            .then(user => res.json(user))
            .catch(err => console.log(err));
        });
      });
    }
  });
});

router.get('/home',(req,res)=>{
        res.sendFile('./home.html',{root:`${__dirname}/../public/`});
})

// Login Route
router.post('/login', (req, res) => {
  const { email, password } = req.body;
  console.log(email, password);

  // Find user by email
  User.findOne({ email }).then(user => {
    // Check if user exists
    if (!user) {
      return res.status(404).json({ emailnotfound: 'Gandu ho tum' });
    }

    // Check password
    bcrypt.compare(password, user.password).then(isMatch => {
      if (isMatch) {
        // User matched
        // Create JWT Payload
        res.redirect("/home")
        // res.sendFile('./home.html',{root:`${__dirname}/../public/`});
        // res.json({ success: true, message: 'Login successful' });
        // res.redirect
      } else {
        return res
          .status(400)
          .json({ passwordincorrect: 'Password incorrect' });
      }
    });
  });
});


router.use(express.static(path.join(__dirname, '..', 'public')));
app.use(router);
module.exports = router;
