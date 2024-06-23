import git
from collections import defaultdict
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np

def get_commit_activity(repo_path):
    repo = git.Repo(repo_path)
    commit_activity = defaultdict(int)
    
    for commit in repo.iter_commits():
        timestamp = commit.committed_datetime
        date_str = timestamp.strftime('%Y-%m-%d')  # Format timestamp as YYYY-MM-DD
        commit_activity[date_str] += 1
    
    return commit_activity

def plot_yearly_contribution_diagrams(commit_activity, output_file):
    # Initialize variables
    start_date = min(commit_activity.keys())
    end_date = max(commit_activity.keys())
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
    end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
    
    current_year = start_datetime.year
    end_year = end_datetime.year
    
    fig, axs = plt.subplots((end_year - current_year + 1), 1, figsize=(26, 4 * (end_year - current_year + 1)), squeeze=False)
    
    for year in range(current_year, end_year + 1):
        # Filter commit activity for the current year
        year_activity = {date: count for date, count in commit_activity.items() if datetime.strptime(date, '%Y-%m-%d').year == year}
        
        if year_activity:
            # Calculate number of days and weeks for the current year
            year_start = datetime(year, 1, 1)
            year_end = datetime(year, 12, 31)
            num_days = (year_end - year_start).days + 1
            num_weeks = num_days // 7 + 1
            
            # Create a 2D array (matrix) to store commit counts for the current year
            contribution_matrix = np.zeros((7, num_weeks))
            
            # Fill the matrix with commit counts for the current year
            for date_str, count in year_activity.items():
                date = datetime.strptime(date_str, '%Y-%m-%d')
                col_index = (date - year_start).days // 7
                row_index = date.weekday()
                contribution_matrix[row_index, col_index] = count
            
            # Plot the contribution diagram for the current year
            ax = axs[year - current_year, 0]
            im = ax.imshow(contribution_matrix, cmap='Greens', interpolation='nearest', aspect='auto')
            
            # Customize plot
            ax.set_title(f'Git Commit Activity - Year {year}')
            ax.set_xlabel('Week of Year')
            ax.set_ylabel('Day of Week (0=Monday, ..., 6=Sunday)')
            fig.colorbar(im, ax=ax, label='Number of Commits')
    
            # Adjusting the tick labels
            week_labels = [year_start + timedelta(weeks=i) for i in range(num_weeks)]
            day_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            ax.set_xticks(np.arange(0, num_weeks))
            ax.set_xticklabels([date.strftime('%b %d') if date.day <= 7 else '' for date in week_labels], rotation=45)
            ax.set_yticks(np.arange(7))
            ax.set_yticklabels(day_labels)
    
    # Adjust layout and save figure
    fig.tight_layout()
    plt.subplots_adjust(hspace=0.5)  # Adjust vertical spacing between subplots
    plt.savefig(output_file)
    plt.show()

if __name__ == "__main__":
    repo_path = '~/your_repo_path'  # Replace with your Git repository path
    output_file = 'diagram.png'  # Output file name for saved figure
    commit_activity = get_commit_activity(repo_path)
    plot_yearly_contribution_diagrams(commit_activity, output_file)
