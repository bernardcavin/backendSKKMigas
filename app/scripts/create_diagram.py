from sqlalchemy import create_engine, MetaData
from sqlalchemy_schemadisplay import create_schema_graph
from sqlalchemy.orm import sessionmaker

import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'

# Replace 'your_database.db' with the path to your SQLite database
DATABASE_URL = 'sqlite:///./test.db'

# Set up SQLAlchemy engine and metadata
engine = create_engine(DATABASE_URL)
metadata = MetaData()
metadata.reflect(bind=engine)

# Generate UML diagram from the reflected metadata
graph = create_schema_graph(
    engine=engine,
    metadata=metadata,
    show_datatypes=False,  # Do not show column data types
    show_indexes=False,    # Do not show indexes
    rankdir='TB',          # From left to right (you can use 'TB' for top to bottom)
    concentrate=True      # Avoid merging lines
)

# Save the diagram to a file
graph.write_png('sqlite_schema_diagram.png')

print("Database diagram saved as 'sqlite_schema_diagram.png'.")