const express = require('express');
const settings = require('./config/settings');
const { initDb, whenReady } = require('./models/database');
const apiRoutes = require('./views/routes');
const errorHandler = require('./middlewares/errorHandler');

initDb();

function createApp() {
  const app = express();

  app.use(express.json());
  app.use(async (req, res, next) => {
    try {
      await whenReady();
      next();
    } catch (err) {
      next(err);
    }
  });
  app.use('/api', apiRoutes);
  app.use(errorHandler);

  return app;
}

const app = createApp();

if (require.main === module) {
  app.listen(settings.port, () => {
    console.log(`Frankenstein LMS rodando na porta ${settings.port}...`);
  });
}

module.exports = { app, createApp };
