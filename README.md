# Michelin Star Restaurant Guide Dashboard

<div align="right"><img alt="plotly" height="31" src="https://images.prismic.io/plotly-marketing-website-2/ce1a4076-4fd2-4040-b99a-aad02fcc2fbb_new-logo-email.png" width="110"></div>

- [Michelin Star Restaurant Guide Dashboard](#michelin-star-restaurant-guide-dashboard)
  - [Plotly Autumn App Challenge 2024](#plotly-autumn-app-challenge-2024)
    - [Dataset](#dataset)
  - [Project Overview](#project-overview)
  - [Features](#features)
  - [Technologies Used](#technologies-used)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Data Source](#data-source)
  - [Project Structure](#project-structure)
  - [Contributing](#contributing)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)
  - [Contact](#contact)

## Plotly Autumn App Challenge 2024

This project is an entry for the Plotly Autumn App Challenge 2024, focusing on creating a Dash app to visualize and analyze data from the Michelin Star Restaurant Guide.

<div align="center"> <img alt="Michelin Star Guide" src="https://images.prismic.io/plotly-marketing-website-2/ZunohrVsGrYSve84_DC16_MichelinStars.png?auto=format,compress" width="400"> </div>

### Dataset

[michelin_by_Jerry_Ng.csv](https://github.com/plotly/datasets/blob/master/michelin_by_Jerry_Ng.csv)

## Project Overview

The goal of this project is to build an interactive dashboard using Plotly's Dash framework and the new MapLibre integration. The app aims to provide insights into Michelin-starred restaurants worldwide, leveraging the dataset provided by Jerry Ng on Kaggle.

## Features

- Interactive map visualization of Michelin-starred restaurants
- Data analysis and insights on restaurant distribution
- User-friendly interface for exploring restaurant information
- Creative use of Plotly's mapping capabilities
- (Optional) Integration of Large Language Models (LLMs) for enhanced data insights

## Technologies Used

- Python
- Plotly Dash
- MapLibre
- Pandas

## Installation

- Clone this repository:

```bash
git clone <repo-uri>
```

- Install the required packages:

```bash
pip install -r requirements.txt
```

- Run the Dash app:

```bash
python app.py
```

## Usage

After running the app, open a web browser and navigate to `http://localhost:8050` to view the dashboard.

## Data Source

The data used in this project is sourced from the Michelin Star Restaurant Guide dataset provided by Jerry Ng on Kaggle.

## Project Structure

- `app.py`: Main application file
- `data/`: Directory containing the dataset
- `assets/`: CSS and other static assets
- `components/`: Reusable Dash components
- `utils/`: Utility functions and helpers

## Contributing

This project is an entry for the Plotly Autumn App Challenge and is not open for contributions. However, feel free to fork the repository and create your own version!

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE.txt) file for details.

## Acknowledgments

- Plotly for organizing the Autumn App Challenge
- Jerry Ng for providing the Michelin Star Restaurant Guide dataset
- The Dash and MapLibre communities for their excellent documentation and support

## Contact

For any questions or feedback, please open an issue in this repository.
