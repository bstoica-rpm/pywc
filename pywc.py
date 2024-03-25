import click 


class DataRow:
    def __init__(self, name):
        self.name = name
        self.lines = 0
        self.bytes = 0
        self.words = 0
        self.chars = 0

    def output(self, show_lines=False, show_chars=False, show_words=False, show_bytes=False):
        num_cols = sum([show_lines, show_chars, show_words, show_bytes])
        fmts = ['{:>8}'] * num_cols
        fmts.append('{:<20}')
        fmt = ' '.join(fmts)

        fields = []
        if(show_lines):
            fields.append(self.lines)
        if(show_chars):
            fields.append(self.chars)
        if(show_words):
            fields.append(self.words)
        if(show_bytes):
            fields.append(self.bytes)

        fields.append(self.name)
        return fmt.format(*fields)
        

@click.command()
@click.argument('inputs', type=click.File('r', encoding='utf-8'), nargs=-1)
@click.option('-c', help='Count bytes in each input file.', is_flag=True)
@click.option('-l', help='Count lines in each input file.', is_flag=True)
@click.option('-m', help='Count characters in each input file.', is_flag=True)
@click.option('-w', help='Count words in each input file.', is_flag=True)
def main(inputs, c, l, m, w):
    """A Python clone of the Unix WC program."""

    if not inputs:
        inputs = [click.get_text_stream('stdin')]

    show_default = not any ([c, l, m, w])
    total_row = DataRow('total')

    header_fields = []
    if(l or show_default):
        header_fields.append('lines')
    if(c or show_default):
        header_fields.append('bytes')
    if(w or show_default):
        header_fields.append('words')
    if(m):
        header_fields.append('chars')
    
    header_fields.append('file')
    header = ' '.join(['{:>8}'.format(field) for field in header_fields])
    click.echo(header)

    for file in inputs:
        row = DataRow(file.name)
        for line in file:
            row.bytes += len(line.encode('utf-8'))
            row.lines += 1
            row.chars += len(line)
            if '\n' in line:
                row.chars += 1  # Count newline as two characters
            row.words += len(line.strip().split())

        total_row.bytes += row.bytes
        total_row.lines += row.lines
        total_row.chars += row.chars
        total_row.words += row.words

        click.echo(row.output(
            show_lines=l or show_default,
            show_bytes=c or show_default,
            show_words=w or show_default,
            show_chars=m,
        ))

    if(len(inputs) > 1):
        click.echo(total_row.output(
            show_lines=l or show_default,
            show_bytes=c or show_default,
            show_words=w or show_default,
            show_chars=m,
        ))


if __name__ == '__main__':
    main()