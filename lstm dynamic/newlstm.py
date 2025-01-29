import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Bidirectional
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import tensorflow as tf
import logging
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import os
from datetime import datetime
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('training.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DynamicConfig:
    def __init__(self, df, target_column=None):
        self.df = df
        self.target_column = target_column
        self.data_length = len(df)

        # Dynamic configurations
        self.sequence_length = self.calculate_sequence_length()
        self.test_size = self.calculate_test_size()
        self.batch_size = self.calculate_batch_size()
        self.epochs = self.calculate_epochs()
        self.layer_units = self.calculate_layer_units()

    def calculate_sequence_length(self):
        return min(60, max(5, int(self.data_length * 0.05)))

    def calculate_test_size(self):
        return min(365, max(30, int(self.data_length * 0.2)))

    def calculate_batch_size(self):
        return min(128, max(32, int(np.sqrt(self.data_length))))

    def calculate_epochs(self):
        return min(50, max(20, int(np.log10(self.data_length) * 20)))

    def calculate_layer_units(self):
        base_units = min(256, max(32, int(np.sqrt(self.data_length) * 4)))
        return [base_units, base_units // 2]


class OutlierHandler:
    def __init__(self):
        self.outliers_info = {}

    def detect_and_handle_outliers(self, data, feature_names):
        clean_data = data.copy()
        for i, feature in enumerate(feature_names):
            Q1 = np.percentile(data[:, i], 25)
            Q3 = np.percentile(data[:, i], 75)
            IQR = Q3 - Q1
            multiplier = 1.5 if abs(np.mean(data[:, i])) < 1000 else 2.0
            lower_bound = Q1 - multiplier * IQR
            upper_bound = Q3 + multiplier * IQR

            outlier_mask = (data[:, i] < lower_bound) | (data[:, i] > upper_bound)
            outlier_indices = np.where(outlier_mask)[0]

            if len(outlier_indices) > 0:
                self.outliers_info[feature] = {
                    'count': len(outlier_indices),
                    'indices': outlier_indices.tolist(),
                    'values': data[outlier_indices, i].tolist(),
                    'bounds': {'lower': lower_bound, 'upper': upper_bound}
                }

                window = min(30, len(data) // 10)
                rolling_median = pd.Series(data[:, i]).rolling(window, center=True).median()
                clean_data[outlier_indices, i] = rolling_median[outlier_indices]

        return clean_data


class DataPreprocessor:
    def __init__(self, config):
        self.config = config
        self.scaler = RobustScaler()
        self.outlier_handler = OutlierHandler()

    def prepare_data(self, save_path=None):
        df = self.config.df.copy()
        date_cols = df.select_dtypes(include=['datetime64']).columns
        if len(date_cols) == 0:
            df['Date'] = pd.to_datetime(df.index if df.index.dtype == 'datetime64[ns]' else df.iloc[:, 0])

        if self.config.target_column:
            self.features = [self.config.target_column]
        else:
            self.features = df.select_dtypes(include=[np.number]).columns.tolist()

        data = df[self.features].values
        clean_data = self.outlier_handler.detect_and_handle_outliers(data, self.features)
        scaled_data = self.scaler.fit_transform(clean_data)

        X, y = [], []
        for i in range(len(scaled_data) - self.config.sequence_length):
            X.append(scaled_data[i:i + self.config.sequence_length])
            y.append(scaled_data[i + self.config.sequence_length])

        X = np.array(X)
        y = np.array(y)

        train_size = len(df) - self.config.test_size
        split_idx = train_size - self.config.sequence_length

        if save_path:
            self.save_outliers(save_path)

        return {
            'X_train': X[:split_idx],
            'y_train': y[:split_idx],
            'X_test': X[split_idx:],
            'y_test': y[split_idx:],
            'scaler': self.scaler,
            'test_dates': df['Date'].values[self.config.sequence_length + split_idx:],
            'feature_names': self.features
        }

    def save_outliers(self, path):
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, 'outliers_info.json'), 'w') as f:
            json.dump(self.outlier_handler.outliers_info, f, indent=4)


class DynamicLSTM:
    def __init__(self, config):
        self.config = config

    def build_model(self, input_shape, n_features):
        model = Sequential()
        for i, units in enumerate(self.config.layer_units):
            if i == 0:
                model.add(Bidirectional(LSTM(
                    units=units,
                    return_sequences=i < len(self.config.layer_units) - 1,
                    input_shape=input_shape
                )))
            else:
                model.add(Bidirectional(LSTM(
                    units=units,
                    return_sequences=i < len(self.config.layer_units) - 1
                )))
            dropout_rate = 0.1 + (i * 0.1)
            model.add(Dropout(dropout_rate))
        model.add(Dense(n_features))
        learning_rate = 0.001 * (1000 / self.config.data_length)
        model.compile(optimizer=Adam(learning_rate=learning_rate), loss='mse')
        return model


class Predictor:
    def __init__(self, df, target_column=None, save_dir='results5'):
        self.config = DynamicConfig(df, target_column)
        self.preprocessor = DataPreprocessor(self.config)
        self.model = DynamicLSTM(self.config)
        self.save_dir = os.path.join(save_dir, datetime.now().strftime('%Y%m%d_%H%M%S'))
        os.makedirs(self.save_dir, exist_ok=True)

    def train_and_predict(self):
        try:
            logger.info("Preparing data...")
            data = self.preprocessor.prepare_data(self.save_dir)

            logger.info("Building and training model...")
            model = self.model.build_model(
                input_shape=(self.config.sequence_length, len(data['feature_names'])),
                n_features=len(data['feature_names'])
            )

            callbacks = [
                EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True),
                ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=1e-6)
            ]

            history = model.fit(
                data['X_train'], data['y_train'],
                epochs=self.config.epochs,
                batch_size=self.config.batch_size,
                validation_split=0.2,
                callbacks=callbacks,
                verbose=1
            )

            logger.info("Generating predictions...")
            predictions = model.predict(data['X_test'])

            self.save_results(data, predictions, history)

            return self.save_dir

        except Exception as e:
            logger.error(f"Error in training and prediction: {str(e)}")
            raise

    def save_results(self, data, predictions, history):
        predictions_unscaled = data['scaler'].inverse_transform(predictions)
        actuals_unscaled = data['scaler'].inverse_transform(data['y_test'])

        results = pd.DataFrame()
        results['Date'] = data['test_dates']

        metrics = {}
        for i, feature in enumerate(data['feature_names']):
            results[f'Actual_{feature}'] = actuals_unscaled[:, i]
            results[f'Predicted_{feature}'] = predictions_unscaled[:, i]

            valid_indices = results[f'Actual_{feature}'].notna() & results[f'Predicted_{feature}'].notna()
            actual_values = results[f'Actual_{feature}'][valid_indices]
            predicted_values = results[f'Predicted_{feature}'][valid_indices]

            if len(actual_values) > 0:
                daily_metrics = pd.DataFrame()
                daily_metrics['Date'] = data['test_dates']
                daily_metrics[f'{feature}_MAE'] = abs(
                    results[f'Actual_{feature}'] - results[f'Predicted_{feature}']
                )
                daily_metrics[f'{feature}_MSE'] = (
                                                          results[f'Actual_{feature}'] - results[f'Predicted_{feature}']
                                                  ) ** 2

                try:
                    metrics[feature] = {
                        'RMSE': float(np.sqrt(mean_squared_error(actual_values, predicted_values))),
                        'MAE': float(mean_absolute_error(actual_values, predicted_values)),
                        'R2': float(r2_score(actual_values, predicted_values)),
                        'Valid_samples': len(actual_values),
                        'Total_samples': len(results),
                        'Missing_samples': len(results) - len(actual_values)
                    }
                except Exception as e:
                    logger.warning(f"Error calculating metrics for {feature}: {str(e)}")
                    metrics[feature] = {
                        'error': str(e),
                        'Valid_samples': len(actual_values),
                        'Total_samples': len(results),
                        'Missing_samples': len(results) - len(actual_values)
                    }

                daily_metrics.to_csv(
                    os.path.join(self.save_dir, f'{feature}_daily_metrics.csv'),
                    index=False
                )

                if len(actual_values) > 0:
                    self.create_visualization(
                        results[valid_indices].copy(),
                        feature,
                        os.path.join(self.save_dir, f'{feature}_predictions.html')
                    )
            else:
                logger.warning(f"No valid data points found for {feature}")
                metrics[feature] = {
                    'error': 'No valid data points found',
                    'Valid_samples': 0,
                    'Total_samples': len(results),
                    'Missing_samples': len(results)
                }

        results.to_csv(os.path.join(self.save_dir, 'predictions.csv'), index=False)
        with open(os.path.join(self.save_dir, 'metrics.json'), 'w') as f:
            json.dump(metrics, f, indent=4)

        pd.DataFrame(history.history).to_csv(
            os.path.join(self.save_dir, 'training_history.csv'),
            index=False
        )

    def create_visualization(self, results, feature, save_path):
        fig = make_subplots(rows=2, cols=1)
        fig.add_trace(
            go.Scatter(
                x=results['Date'],
                y=results[f'Actual_{feature}'],
                name='Actual',
                line=dict(color='blue')
            ),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(
                x=results['Date'],
                y=results[f'Predicted_{feature}'],
                name='Predicted',
                line=dict(color='red')
            ),
            row=1, col=1
        )
        error = results[f'Predicted_{feature}'] - results[f'Actual_{feature}']
        fig.add_trace(
            go.Scatter(
                x=results['Date'],
                y=error,
                name='Prediction Error',
                line=dict(color='green')
            ),
            row=2, col=1
        )
        fig.update_layout(height=800, title_text=f"{feature} Predictions and Error")
        fig.write_html(save_path)


# Example usage
if __name__ == "__main__":
    df = pd.read_csv('bitcoin_10_yearsdata.csv')
    predictor = Predictor(df, target_column='Close')
    results_dir = predictor.train_and_predict()
    print(f"Results saved to: {results_dir}")