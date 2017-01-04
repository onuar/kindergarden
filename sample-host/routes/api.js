var express = require('express');
var router = express.Router();

router.get('/get', function(req, res, next) {
  res.send('api/get');
});

router.post('/post', function(req, res, next) {
  res.send('api/post');
});

router.put('/put', function(req, res, next) {
  res.send('api/put');
});

router.patch('/patch', function(req, res, next) {
  res.send('api/patch');
});

router.delete('/delete', function(req, res, next) {
  res.send('api/delete');
});

module.exports = router;
