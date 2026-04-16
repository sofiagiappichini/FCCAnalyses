import ROOT
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.interpolate import griddata

# Function to read data from a ROOT file and extract a 2D histogram
def read_root_histogram(file_path, hist_name):
    # Open the ROOT file
    root_file = ROOT.TFile.Open(file_path)
    if not root_file or root_file.IsZombie():
        raise FileNotFoundError(f"Could not open ROOT file: {file_path}")

    # Get the histogram
    hist = root_file.Get(hist_name)
    if not hist:
        raise ValueError(f"Histogram '{hist_name}' not found in file: {file_path}")

    # Extract bin edges and values
    x_bins = hist.GetNbinsX()
    y_bins = hist.GetNbinsY()

    x_edges = [hist.GetXaxis().GetBinLowEdge(i) for i in range(1, x_bins + 2)]
    y_edges = [hist.GetYaxis().GetBinLowEdge(i) for i in range(1, y_bins + 2)]

    values = np.array([[hist.GetBinContent(i, j) for j in range(1, y_bins + 1)] for i in range(1, x_bins + 1)])

    root_file.Close()
    return np.array(x_edges), np.array(y_edges), values

# Function to read data from a ROOT file and extract a 2D graph (TGraph2D)
def read_root_graph(file_path, graph_name):
    # Open the ROOT file
    root_file = ROOT.TFile.Open(file_path)
    if not root_file or root_file.IsZombie():
        raise FileNotFoundError(f"Could not open ROOT file: {file_path}")

    # Get the graph
    graph = root_file.Get(graph_name)
    if not graph or not isinstance(graph, ROOT.TGraph2D):
        raise ValueError(f"Graph '{graph_name}' not found or is not a TGraph2D in file: {file_path}")

    # Extract points from the graph
    n_points = graph.GetN()
    x = np.array([graph.GetX()[i] for i in range(n_points)])
    y = np.array([graph.GetY()[i] for i in range(n_points)])
    z = np.array([graph.GetZ()[i] for i in range(n_points)])

    root_file.Close()
    return x, y, z

# Adjust the interpolation to ensure compatibility with pcolormesh
def interpolate_to_grid(x, y, z, grid_size=100):
    # Define grid edges
    x_min, x_max = x.min(), x.max()
    y_min, y_max = y.min(), y.max()
    grid_x = np.linspace(x_min, x_max, grid_size + 1)  # Add 1 to ensure correct dimensions
    grid_y = np.linspace(y_min, y_max, grid_size + 1)  # Add 1 to ensure correct dimensions
    grid_X, grid_Y = np.meshgrid(grid_x, grid_y, indexing='ij')

    # Interpolate z values onto the grid
    grid_Z = griddata((x, y), z, (grid_X[:-1, :-1], grid_Y[:-1, :-1]), method='linear')
    return grid_X, grid_Y, grid_Z

# Update the plotting function to increase the font size of axis labels and ticks
def plot_2d_with_contours(grid_X, grid_Y, grid_Z, contour_levels, output_path):
    # Plot the 2D histogram as a color map
    plt.figure(figsize=(8, 6))
    cmap = plt.colormaps['BuPu_r']  # Use the inverted 'BuPu' colormap with the new API
    mesh = plt.pcolormesh(grid_X, grid_Y, grid_Z, cmap=cmap, shading='auto', rasterized=True)  # Rasterize to avoid grid artifacts
    cbar = plt.colorbar(mesh)
    cbar.set_label(r'$-2\Delta\ln L$', fontsize=14)  # Increase font size of colorbar label
    cbar.ax.tick_params(labelsize=12)  # Increase font size of colorbar ticks

    # Add contour lines with custom styles
    contour_1sigma = plt.contour(grid_X[:-1, :-1], grid_Y[:-1, :-1], grid_Z, levels=[contour_levels[0]], colors='white', linestyles='solid', linewidths=2)
    contour_2sigma = plt.contour(grid_X[:-1, :-1], grid_Y[:-1, :-1], grid_Z, levels=[contour_levels[1]], colors='white', linestyles='dotted', linewidths=2)

    # Add labels directly on the contour lines
    plt.clabel(contour_1sigma, inline=True, fontsize=14, fmt={contour_levels[0]: r'$1\sigma$'})
    plt.clabel(contour_2sigma, inline=True, fontsize=14, fmt={contour_levels[1]: r'$2\sigma$'})

    # Add a bold white cross at (0, 0) and a text label
    plt.plot(0, 0, marker='x', color='white', markersize=10, markeredgewidth=2)
    plt.text(0.05, -0.025, "Expected", color='white', fontsize=12, ha='left', va='bottom')

    # Add labels and title
    plt.xlabel(r"$Im(C_{eH})$", fontsize=14)
    plt.ylabel(r"$Re(C_{eH})$", fontsize=14)
    plt.xticks(fontsize=14)  # Increase font size of x-axis ticks
    plt.yticks(fontsize=14)
    plt.ylim(-0.6,0.6)
    plt.gcf().text(0.75, 0.93, "FCC-ee Simulation (Delphes)", fontsize=15, va='top', ha='right', fontweight='bold', transform=plt.gcf().transFigure)

    # Save the plot
    plt.savefig(output_path+'.png', bbox_inches='tight', dpi=330)
    plt.savefig(output_path+'.pdf', bbox_inches='tight')
    plt.close()

# Define contour levels for the plot
contour_levels = [2.3, 5.99]  # Values for the two contour lines

# Example usage
if __name__ == "__main__":
    # Define the ROOT file and graph name
    root_file_path = "/afs/cern.ch/user/m/mpresill/public/scan_cehim_cehre_linear.root"  # Replace with your ROOT file path
    graph_name = "Main"          # Replace with your TGraph2D name

    # Read the graph data
    try:
        x, y, z = read_root_graph(root_file_path, graph_name)
    except (FileNotFoundError, ValueError) as e:
        print(e)
        exit(1)

    # Interpolate the data to a grid
    grid_X, grid_Y, grid_Z = interpolate_to_grid(x, y, z)

    # Define the output path for the plot
    output_plot_path = "/eos/user/s/sgiappic/www/Higgs_CP/ecm240/EFT/2d_scan"  # Replace with your desired output path

    # Plot the 2D graph with contours
    plot_2d_with_contours(grid_X, grid_Y, grid_Z, contour_levels, output_plot_path)

    print(f"Plot saved to {output_plot_path}")