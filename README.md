**Shortest-Path-Finder**

Shortest-Path-Finder is a Python-based tool designed to calculate the most efficient path between nodes in a graph, considering factors such as slope and distance. Additionally, it offers a feature to generate circular routes of specified lengths.

**Features**

- Customizable Weight Functions: Incorporates various weight functions to adjust path calculations based on slope and distance.
- Slope-Based Pathfinding: Selects appropriate weight functions according to slope values to determine optimal paths.
- Circular Route Generation: Generates circular routes of specified lengths, ideal for planning circular trips or tours.

**Installation**
1. Clone the Repository:

		git clone https://github.com/yourusername/Shortest-Path-Finder.git
2. Go to the folder

		cd Shortest-Path-Finder


3. Set Up a Virtual Environment (Optional but recommended):

		python -m venv env
		source env/bin/activate  # On Windows: env\Scripts\activate

5. Install Dependencies:

		pip install -r requirements.txt

**Usage**

1. Import the Desired Weight Function:

		from weightFuncFactory import combined_weight_and_distance

2. Calculate the Weight:

		slope = 0.05  # Example slope value
		factor = 2    # Example factor
		distance = 100  # Distance between nodes

		weight = combined_weight_and_distance(slope, factor, distance)


3. Generate a Circular Route:

		from weightFuncFactory import calculate_circular_route

		start_node = 'A'  # Starting point
		desired_length = 10  # Desired length of the circular route in kilometers
		
		circular_route = calculate_circular_route(start_node, desired_length)

**Parameters:**

- start_node: The starting point of the route.
- desired_length: The desired length of the circular route in kilometers.
  
**Notes:**
- Ensure that your graph contains sufficient nodes and edges to accommodate the desired route length.
- The function aims to match the specified length as closely as possible; however, slight deviations may occur depending on the graph’s structure.

**Contributing:**

Contributions are welcome! Please fork the repository and create a pull request with your enhancements or bug fixes.

**License**

This project is licensed under the MIT License. See the LICENSE file for details.

**Acknowledgments**

Special thanks to all contributors and the open-source community for their invaluable support and resources.
