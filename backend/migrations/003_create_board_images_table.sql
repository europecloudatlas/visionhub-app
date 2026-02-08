-- Create board_images table
CREATE TABLE IF NOT EXISTS board_images (
    id SERIAL PRIMARY KEY,
    board_id INTEGER NOT NULL,
    image_url VARCHAR(500) NOT NULL,
    filename VARCHAR(255) NOT NULL,
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    CONSTRAINT fk_board_images_board_id FOREIGN KEY (board_id) 
        REFERENCES boards(id) 
        ON DELETE CASCADE
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_board_images_board_id ON board_images(board_id);
CREATE INDEX IF NOT EXISTS idx_board_images_uploaded_at ON board_images(uploaded_at DESC);

-- Add comment
COMMENT ON TABLE board_images IS 'Images associated with vision boards';