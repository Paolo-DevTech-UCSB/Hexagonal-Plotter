# -*- coding: utf-8 -*-
"""
Module Assembly Plots - PostgreSQL Survey Data to Plots Converter
Uses PGConnect.py to retrieve survey data from PostgreSQL and creates plots using plotter_code_clean.py
Follows the exact same approach as 3D_height_V11.py and New_Controller.py
"""

import PGConnect
from plotter_code_clean import Make_Diff_Plot


class PostgresPlotter:
    """Handles retrieval of survey data from PostgreSQL and plot generation using Make_Diff_Plot"""
    
    def __init__(self, module_name, shape_id='LDF', folder_path='./'):
        """
        Initialize the plotter
        
        Args:
            module_name (str): The module name to query from database
            shape_id (str): The hexagonal shape ID (LDF, HDF, LDR, LDL, LDT, LDB, HDT, HDB)
            folder_path (str): Base folder path for output (used by Make_Diff_Plot)
        """
        self.module_name = module_name
        self.shape_id = shape_id
        self.folder_path = folder_path
    
    def get_pg_data(self, module_name, sort="newest"):
        """
        Retrieve survey data for a module from PostgreSQL using PGConnect
        
        Args:
            module_name (str): Module name to retrieve
            sort (str): 'newest' or 'oldest' to get specific entry
            
        Returns:
            dict: Heightlist data compatible with Make_Diff_Plot
        """
        try:
            pg_data = PGConnect.main(module_name, sort=sort)
            return pg_data
        except Exception as e:
            print(f"Error retrieving data for {module_name}: {e}")
            return None
    
    def create_shape_plot(self, module_name, output_filename=None):
        """
        Create a shape plot for a single survey entry
        
        Args:
            module_name (str): Module name to plot
            output_filename (str): Output filename for the plot
        """
        if output_filename is None:
            output_filename = f"{module_name}_shape_plot.png"
        
        print(f"\nCreating shape plot for {module_name}...")
        
        # Get PostgreSQL data
        pg_data = self.get_pg_data(module_name, sort="newest")
        
        if pg_data is None:
            print(f"Could not retrieve data for {module_name}")
            return
        
        # Use Make_Diff_Plot with the same data twice for single plot (ShapePlot=True)
        Make_Diff_Plot(pg_data, pg_data, self.folder_path, module_name, module_name, 
                      self.shape_id, ShapePlot=True, FileName=output_filename)
        
        print(f"Shape plot saved: {output_filename}")
    
    def create_difference_plot(self, module_name_1, module_name_2=None, output_filename=None):
        """
        Create individual shape plots for F (final) and I (initial), plus their difference plot
        
        Args:
            module_name_1 (str): First module name (or module name if module_name_2 is None)
            module_name_2 (str): Second module name (optional - if None, uses same module with different entries)
            output_filename (str): Output filename for the difference plot
        """
        if module_name_2 is None:
            module_name_2 = module_name_1
        
        print(f"\n{'='*60}")
        print(f"Creating Final/Initial comparison plots")
        print(f"{'='*60}\n")
        
        # Get PostgreSQL data for both modules
        pg_data_final = self.get_pg_data(module_name_1, sort="newest")
        pg_data_initial = self.get_pg_data(module_name_2, sort="oldest")
        
        if pg_data_final is None or pg_data_initial is None:
            print(f"Could not retrieve data for one or both modules")
            return
        
        # Create Final (F) shape plot
        print("\n--- Creating Final (F) Shape Plot ---")
        final_filename = f"{module_name_1}_F_final_shape.png"
        Make_Diff_Plot(pg_data_final, pg_data_final, self.folder_path, module_name_1, module_name_1, 
                      self.shape_id, ShapePlot=True, FileName=final_filename)
        print(f"Final shape plot saved: {final_filename}")
        
        # Create Initial (I) shape plot
        print("\n--- Creating Initial (I) Shape Plot ---")
        initial_filename = f"{module_name_2}_I_initial_shape.png"
        Make_Diff_Plot(pg_data_initial, pg_data_initial, self.folder_path, module_name_2, module_name_2, 
                      self.shape_id, ShapePlot=True, FileName=initial_filename)
        print(f"Initial shape plot saved: {initial_filename}")
        
        # Create Difference (F - I) plot
        print("\n--- Creating Difference (F - I) Plot ---")
        if output_filename is None:
            output_filename = f"{module_name_1}_vs_{module_name_2}_difference.png"
        
        Make_Diff_Plot(pg_data_final, pg_data_initial, self.folder_path, module_name_1, module_name_2, 
                      self.shape_id, ShapePlot=False, FileName=output_filename)
        print(f"Difference plot saved: {output_filename}")
        
        print(f"\n{'='*60}")
        print(f"All plots complete!")
        print(f"{'='*60}\n")


def main():
    """
    Example usage: Retrieve and plot survey data for modules
    Creates three plots: Final shape, Initial shape, and Difference (F-I)
    """
    # Configuration
    MODULE_NAME = "320MHF2TDSB0255" # Change this to your module name
    SHAPE_ID = "HDF"  # Change this to match your module shape
    FOLDER_PATH = "./"  # Output folder
    
    # Create plotter instance
    plotter = PostgresPlotter(MODULE_NAME, shape_id=SHAPE_ID, folder_path=FOLDER_PATH)
    
    # Create Final (F), Initial (I), and Difference (F-I) plots all at once
    plotter.create_difference_plot(MODULE_NAME)
    
    # To compare two different modules:
    # plotter.create_difference_plot("MODULE_NAME_1", "MODULE_NAME_2")


if __name__ == "__main__":
    main()
    
    # Alternative: Direct usage example
    """
    plotter = PostgresPlotter("320MHF2TDSB0252", shape_id="HDF")
    
    # Create Final (F), Initial (I), and Difference (F-I) plots
    plotter.create_difference_plot("320MHF2TDSB0252")
    
    # Compare two different modules
    plotter.create_difference_plot("MODULE_A", "MODULE_B")
    
    # Create only a single shape plot for a module
    plotter.create_shape_plot("320MHF2TDSB0252", output_filename="single_shape_plot.png")
    """
