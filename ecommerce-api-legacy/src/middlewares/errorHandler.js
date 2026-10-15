function errorHandler(err, req, res, next) {
  console.error('[ERROR]', err.message || err);
  if (res.headersSent) {
    return next(err);
  }
  res.status(500).send('Erro interno do servidor');
}

module.exports = errorHandler;
